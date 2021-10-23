from web_messaging.blueprints.billing.storage import (
    delete_file_from_temporary_folder, upload_file_to_gcp,
    upload_file_to_temporary_folder)


class Bill():

    def __init__(self, date, total_cost_usd, file, path_to_gcs=None):
        self.file = file
        self.date = date
        self.filename = self.file.filename
        self.total_cost_usd = total_cost_usd
        self.total_cost_eur = None
        self.path_to_gcs = path_to_gcs
        self.set_total_cost_eur()

    def dict(self):
        return {
            "date": self.date,
            "filename": self.filename,
            "total_cost_usd": self.total_cost_usd,
            "total_cost_eur": self.total_cost_eur,
            "path_to_gcs": self.path_to_gcs
        }

    def set_total_cost_eur(self):
        total_cost_eur = self.total_cost_usd * 0.85
        self.total_cost_eur = total_cost_eur

    def upload_to_gcs(self):
        local_path = upload_file_to_temporary_folder(self.file, self.filename)
        gcs_file_path = upload_file_to_gcp(local_path, self.filename)
        self.path_to_gcs = gcs_file_path
        delete_file_from_temporary_folder(local_path)
        return gcs_file_path
