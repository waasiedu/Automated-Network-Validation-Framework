import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_OF_TRUTH_DIR = BASE_DIR / "source_of_truth"
REPORTS_DIR = BASE_DIR / "reports"

DEVICES_FILE = SOURCE_OF_TRUTH_DIR / "devices.yaml"
SITES_FILE = SOURCE_OF_TRUTH_DIR / "sites.yaml"
VALIDATION_CHECKS_FILE = SOURCE_OF_TRUTH_DIR / "validation_checks.yaml"

TEXT_REPORT_FILE = REPORTS_DIR / "validation_report.txt"
JSON_REPORT_FILE = REPORTS_DIR / "validation_report.json"

NETBOX_URL = os.getenv("NETBOX_URL")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")