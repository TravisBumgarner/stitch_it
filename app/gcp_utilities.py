from google.cloud import storage
import uuid

def save_to_bucket(html_body):
    client = storage.Client()
    bucket = client.get_bucket("test_stitching")
    blob = storage.Blob(f'{uuid.uuid4().hex}.html', bucket)
    blob.upload_from_string(html_body, "text/html")