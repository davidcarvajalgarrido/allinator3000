# Cloud Run Function: renombrar ficheros en GCS con hash MD5

Guía basada en los pasos reales seguidos para desplegar una Cloud Run Function (gen2) que renombra automáticamente cualquier fichero subido a un bucket de Google Cloud Storage usando su hash MD5 como nombre.

---

## Qué hace la función

Cuando se sube un fichero al bucket `gs://allinator-files`, la función:

1. Se dispara automáticamente mediante un trigger de Eventarc.
2. Descarga el contenido del fichero.
3. Calcula su hash MD5 (32 caracteres hexadecimales).
4. Renombra el fichero conservando la extensión original.
5. Elimina el fichero con el nombre original.

Ejemplo: `basilisco.jpg` → `be1ea26cb65d914cd13cb72c0935c01b.jpg`

---

## Requisitos previos

- `gcloud` CLI instalado y autenticado (`gcloud auth login` y `gcloud auth application-default login`)
- Python 3.11+ con `venv` disponible
- Proyecto de GCP con facturación activa
- Permisos de propietario (`roles/owner`) sobre el proyecto

---

## 1. Estructura del proyecto

```
pics-manager/
├── .venv/                    # Entorno virtual Python (no se sube a Git)
├── list_files.py             # Script auxiliar para listar el bucket
└── rename_function/
    ├── main.py               # Código de la Cloud Run Function
    └── requirements.txt      # Dependencias Python de la función
```

---

## 2. Crear el entorno virtual

```bash
cd pics-manager
python3 -m venv .venv
source .venv/bin/activate
pip install google-cloud-storage
```

---

## 3. Código de la función

**`rename_function/main.py`**

```python
import hashlib
import os

import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import storage


@functions_framework.cloud_event
def rename_on_upload(cloud_event: CloudEvent):
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]

    # Evitar bucle infinito: ignorar ficheros ya renombrados con hash
    name_without_ext, ext = os.path.splitext(file_name)
    if len(name_without_ext) == 32 and all(c in "0123456789abcdef" for c in name_without_ext):
        print(f"Ignorado (ya tiene nombre hash): {file_name}")
        return

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Calcular MD5 del contenido (32 caracteres hexadecimales)
    content = blob.download_as_bytes()
    hash_name = hashlib.md5(content).hexdigest()
    new_name = hash_name + ext

    # Copiar con el nuevo nombre y eliminar el original
    bucket.copy_blob(blob, bucket, new_name)
    blob.delete()

    print(f"Renombrado: {file_name} -> {new_name}")
```

**`rename_function/requirements.txt`**

```
functions-framework==3.*
google-cloud-storage==2.*
```

---

## 4. Comprobar la región del bucket

Antes de desplegar, hay que conocer la región del bucket porque el trigger de Eventarc **debe estar en la misma región**:

```bash
gsutil ls -L -b gs://allinator-files | grep "Location constraint"
```

En este caso devuelve `US` (multi-región), lo que implica usar `--trigger-location=us` en el deploy y elegir una región individual de `us-*` para la función.

---

## 5. Asignar los permisos necesarios

Este es el paso más crítico. Son necesarios **cuatro** roles sobre distintas cuentas de servicio. Sin ellos el deploy o la ejecución fallarán.

Obtén primero el número de proyecto:

```bash
gcloud projects describe TU_PROJECT_ID --format="value(projectNumber)"
```

### 5.1. Cloud Build: permiso para construir la función

```bash
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"
```

### 5.2. Eventarc: permiso para recibir eventos

```bash
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/eventarc.eventReceiver"
```

### 5.3. GCS → Pub/Sub: el agente de Cloud Storage necesita publicar eventos

```bash
# Obtener la cuenta de servicio del agente de GCS
GCS_SA=$(gsutil kms serviceaccount -p TU_PROJECT_ID)

gcloud projects add-iam-policy-binding TU_PROJECT_ID \
  --member="serviceAccount:${GCS_SA}" \
  --role="roles/pubsub.publisher"
```

### 5.4. Cloud Run: permiso para que Eventarc invoque el servicio

Este permiso se añade **sobre el servicio Cloud Run** (no sobre el proyecto), y solo se puede hacer después del primer deploy:

```bash
gcloud run services add-iam-policy-binding rename-on-upload \
  --region=us-east1 \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --project=TU_PROJECT_ID
```

> **Nota:** La propagación de cambios IAM puede tardar varios minutos. Si la función sigue fallando justo después de añadir un permiso, espera un par de minutos y vuelve a probar.

---

## 6. Desplegar la función

```bash
gcloud functions deploy rename-on-upload \
  --gen2 \
  --runtime=python311 \
  --region=us-east1 \
  --source=pics-manager/rename_function \
  --entry-point=rename_on_upload \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=allinator-files" \
  --trigger-location=us \
  --project=TU_PROJECT_ID
```

Puntos clave del comando:

- `--gen2`: necesario para usar Eventarc como trigger.
- `--region`: región donde corre la función (debe ser una región dentro de la multi-región del bucket).
- `--trigger-location`: debe coincidir con la región/multi-región del bucket (`us`, `europe`, `asia` o una región específica).

---

## 7. Verificar el despliegue

```bash
gcloud functions describe rename-on-upload \
  --region=us-east1 \
  --project=TU_PROJECT_ID
```

El campo `state` debe ser `ACTIVE`.

---

## 8. Probar la función

Sube cualquier fichero al bucket:

```bash
gsutil cp ~/ruta/al/fichero.jpg gs://allinator-files/fichero.jpg
```

Espera unos 30 segundos y lista el bucket:

```bash
gsutil ls gs://allinator-files/
```

El fichero original habrá desaparecido y en su lugar aparecerá uno con nombre de 32 caracteres hexadecimales y la misma extensión.

---

## Resumen de comandos (todo junto)

```bash
# Variables
PROJECT_ID="TU_PROJECT_ID"
PROJECT_NUMBER="TU_PROJECT_NUMBER"
BUCKET="allinator-files"
FUNCTION_NAME="rename-on-upload"
REGION="us-east1"
TRIGGER_LOCATION="us"  # debe coincidir con la región del bucket

# 1. Permisos Cloud Build
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

# 2. Permisos Eventarc
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/eventarc.eventReceiver"

# 3. Permisos Pub/Sub para el agente de GCS
GCS_SA=$(gsutil kms serviceaccount -p $PROJECT_ID)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${GCS_SA}" \
  --role="roles/pubsub.publisher"

# 4. Desplegar
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=pics-manager/rename_function \
  --entry-point=rename_on_upload \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=${BUCKET}" \
  --trigger-location=$TRIGGER_LOCATION \
  --project=$PROJECT_ID

# 5. Permiso Cloud Run invoker (después del primer deploy)
gcloud run services add-iam-policy-binding $FUNCTION_NAME \
  --region=$REGION \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --project=$PROJECT_ID

# 6. Probar
gsutil cp ~/Descargas/basilisco.jpg gs://${BUCKET}/basilisco.jpg
sleep 30
gsutil ls gs://${BUCKET}/
```
