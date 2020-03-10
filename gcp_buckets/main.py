from google.cloud import storage
from flask import render_template, flash, redirect, request
from flask import Flask

app = Flask(__name__)

def upload_blob(bucket_name='test_stitching', source_file_name='foo.txt', destination_blob_name='bar.txt'):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    return upload_blob()

