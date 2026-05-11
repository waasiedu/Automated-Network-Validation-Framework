import yaml

from src.config.settings import VALIDATION_CHECKS_FILE


class ValidationPolicy:
    def __init__(self, validation_checks_file=VALIDATION_CHECKS_FILE):
        self.validation_checks_file = validation_checks_file

    def get_validation_checks(self):
        with open(self.validation_checks_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data.get("checks", []) if data else []