import yaml

from src.config.settings import DEVICES_FILE, SITES_FILE, VALIDATION_CHECKS_FILE
from src.sources.base import SourceOfTruth


class YAMLSource(SourceOfTruth):
    def __init__(
        self,
        devices_file=DEVICES_FILE,
        sites_file=SITES_FILE,
        validation_checks_file=VALIDATION_CHECKS_FILE,
    ):
        self.devices_file = devices_file
        self.sites_file = sites_file
        self.validation_checks_file = validation_checks_file

    def _load_yaml(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data or {}

    def get_sites(self):
        data = self._load_yaml(self.sites_file)
        return data.get("sites", [])

    def get_devices(self):
        data = self._load_yaml(self.devices_file)
        return data.get("devices", [])

   