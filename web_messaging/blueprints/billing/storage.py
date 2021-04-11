
from web_messaging.extensions import gcp_storage
from config.settings import UPLOAD_FOLDER, GCS_BILLING_BUCKET
import os 


def upload_file_to_temporary_folder(file):
    filename = file.filename
    file_local_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(file_local_path)
    except Exception as e:
        return str(e)
    return file_local_path


def upload_file_to_gcp(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    bucket = gcp_storage.bucket(GCS_BILLING_BUCKET)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )