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
