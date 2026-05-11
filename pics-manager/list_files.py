from google.cloud import storage

def list_bucket_files(bucket_name: str, project: str) -> list[str]:
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    blobs = client.list_blobs(bucket)
    return [blob.name for blob in blobs]

if __name__ == "__main__":
    PROJECT = "project-f59f1919-9922-4f77-a63"
    BUCKET = "allinator-files"

    files = list_bucket_files(BUCKET, PROJECT)
    print(f"{len(files)} ficheros encontrados:")
    for f in files:
        print(f)
