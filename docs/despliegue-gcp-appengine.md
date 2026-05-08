# Despliegue en Google App Engine (Node.js)

Guía basada en los problemas reales encontrados al desplegar por primera vez una app Node.js en Google App Engine Standard. La documentación oficial de Google omite varios de estos pasos.

---

## Requisitos previos

- `gcloud` CLI instalado y autenticado (`gcloud auth login`)
- Proyecto de GCP creado con facturación activa
- App Engine inicializado en el proyecto (`gcloud app create`)

---

## 1. Estructura mínima del proyecto

Necesitas al menos estos tres archivos:

```
mi-app/
├── app.yaml
├── package.json
└── server.js
```

---

## 2. Configurar `app.yaml` correctamente

Un `app.yaml` con solo `runtime: nodejs22` **no es suficiente**. Necesitas especificar también el entorno y el entrypoint:

```yaml
runtime: nodejs22

env: standard

entrypoint: node server.js

env_variables:
  NODE_ENV: production
```

Sin `entrypoint`, App Engine no sabe cómo arrancar tu aplicación. Sin `env: standard`, puede haber ambigüedad en el tipo de entorno.

---

## 3. Primer intento de despliegue

```bash
gcloud app deploy
```

Este comando fallará con un error de permisos en Cloud Build (ver sección siguiente).

---

## 4. Problema: permisos de Artifact Registry

### El error

El build falla con este mensaje en los logs de Cloud Build:

```
ERROR: failed to initialize analyzer: validating registry write access:
failed to ensure registry read/write access to eu.gcr.io/...
DENIED: Permission 'artifactregistry.repositories.uploadArtifacts' denied
```

### Qué está pasando

Desde 2023, Google migró `eu.gcr.io` (y todos los registros `*.gcr.io`) para que estén respaldados internamente por **Artifact Registry**. Esto significa que:

- El repositorio `eu.gcr.io` en Artifact Registry **debe existir explícitamente** en tu proyecto.
- Las cuentas de servicio involucradas en el build **deben tener permisos** para subir imágenes a ese repositorio.

La documentación oficial de App Engine **no menciona este requisito** en el flujo de despliegue estándar.

---

## 5. Solución: habilitar APIs y asignar permisos

### 5.1. Habilitar Artifact Registry API

```bash
gcloud services enable artifactregistry.googleapis.com \
  --project=TU_PROJECT_ID
```

### 5.2. Identificar las cuentas de servicio involucradas

Hay **tres** cuentas de servicio relevantes (no confundirlas entre sí):

| Cuenta | Propósito |
|---|---|
| `PROJECT_NUMBER@cloudbuild.gserviceaccount.com` | Ejecuta los pasos del build |
| `service-PROJECT_NUMBER@gcp-sa-cloudbuild.iam.gserviceaccount.com` | Service agent interno de Cloud Build |
| `PROJECT_ID@appspot.gserviceaccount.com` | Cuenta de servicio de App Engine |

Puedes ver qué cuentas y roles tiene tu proyecto con:

```bash
gcloud projects get-iam-policy TU_PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role,bindings.members)" \
  --filter="bindings.members:cloudbuild OR bindings.members:appspot"
```

### 5.3. Asignar `artifactregistry.writer` a las cuentas necesarias

```bash
# Cuenta principal de Cloud Build
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Service agent interno de Cloud Build (¡esta es la que faltaba!)
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-cloudbuild.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Cuenta de servicio de App Engine
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

> **Nota:** Sustituye `TU_PROJECT_ID` por el ID de tu proyecto (ej. `mi-proyecto-123`) y `PROJECT_NUMBER` por el número numérico del proyecto (ej. `1041160808171`). Puedes obtenerlos con `gcloud projects describe TU_PROJECT_ID`.

### 5.4. Asignar `storage.admin` a las cuentas de build

App Engine también usa Cloud Storage durante el despliegue:

```bash
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/storage.admin"
```

---

## 6. Crear el repositorio `eu.gcr.io` en Artifact Registry

Aunque `eu.gcr.io` parece un registro de contenedores "clásico", en realidad es un repositorio de Artifact Registry que **debe crearse manualmente** la primera vez:

```bash
gcloud artifacts repositories create "eu.gcr.io" \
  --repository-format=DOCKER \
  --location=europe \
  --project=TU_PROJECT_ID
```

Si el repositorio ya existe, el comando devolverá un error que puedes ignorar. Si tu región no es Europa, usa `us` o `asia` en `--location` según corresponda, y el prefijo del repositorio cambiará a `us.gcr.io` o `asia.gcr.io`.

---

## 7. Desplegar de nuevo

Con todo lo anterior configurado:

```bash
gcloud app deploy
```

Esta vez el build debería completarse con éxito.

---

## 8. Verificar que la app está funcionando

```bash
gcloud app browse
```

Abre automáticamente la URL de tu app en el navegador.

---

## Resumen de comandos (todo junto)

```bash
# Variables (ajusta estos valores)
PROJECT_ID="TU_PROJECT_ID"
PROJECT_NUMBER="TU_PROJECT_NUMBER"

# 1. Habilitar APIs
gcloud services enable artifactregistry.googleapis.com --project=$PROJECT_ID

# 2. Permisos Artifact Registry
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-cloudbuild.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_ID}@appspot.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# 3. Permisos Storage
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_ID}@appspot.gserviceaccount.com" \
  --role="roles/storage.admin"

# 4. Crear repositorio en Artifact Registry
gcloud artifacts repositories create "eu.gcr.io" \
  --repository-format=DOCKER \
  --location=europe \
  --project=$PROJECT_ID

# 5. Desplegar
gcloud app deploy
```
