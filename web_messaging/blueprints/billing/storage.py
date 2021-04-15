
from web_messaging.extensions import gcp_storage
from config.settings import UPLOAD_FOLDER, GCS_BILLING_BUCKET
import os


def retrieve_file_from_bucket(filename):
    bucket = gcp_storage.get_bucket(GCS_BILLING_BUCKET)
    blob = bucket.blob(filename)
    file_local_path = os.path.join('web_messaging/', UPLOAD_FOLDER, filename)
    blob.download_to_filename(file_local_path)
    return f'tmp/{filename}'


def upload_file_to_temporary_folder(file, filename):
    """ Upload a file to a local storage """
    file_local_path = os.path.join('web_messaging/', UPLOAD_FOLDER, filename)
    try:
        file.save(file_local_path)
    except Exception as e:
        return str(e)
    return file_local_path


def delete_file_from_temporary_folder(filename):
    """ Upload a file to a local storage """
    os.remove(filename)


def upload_file_to_gcp(source_file_name, destination_blob_name):
    """ Upload a file to a GCS bucket """
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
    return f'gs://{GCS_BILLING_BUCKET}/{destination_blob_name}'
