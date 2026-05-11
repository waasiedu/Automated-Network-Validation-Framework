import json
from datetime import datetime, timezone

from src.config.settings import JSON_REPORT_FILE, REPORTS_DIR, TEXT_REPORT_FILE


class ReportWriter:
    def __init__(
        self,
        text_report_file=TEXT_REPORT_FILE,
        json_report_file=JSON_REPORT_FILE,
    ):
        self.text_report_file = text_report_file
        self.json_report_file = json_report_file

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def write_reports(self, results):
        report_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": self._build_summary(results),
            "results": results,
        }

        self._write_text_report(report_data)
        self._write_json_report(report_data)

        return {
            "text_report": str(self.text_report_file),
            "json_report": str(self.json_report_file),
        }

    def _build_summary(self, results):
        total_devices = len(results)
        total_checks = 0
        passed_checks = 0
        failed_checks = 0

        for device_result in results:
            for check_result in device_result.get("checks", []):
                total_checks += 1

                if check_result.get("status") == "PASS":
                    passed_checks += 1
                else:
                    failed_checks += 1

        overall_status = "PASS" if failed_checks == 0 else "FAIL"

        return {
            "overall_status": overall_status,
            "total_devices": total_devices,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
        }

    def _write_text_report(self, report_data):
        summary = report_data["summary"]
        results = report_data["results"]

        lines = [
            "Network Validation Report",
            "=" * 25,
            f"Generated At: {report_data['generated_at']}",
            f"Overall Status: {summary['overall_status']}",
            f"Total Devices: {summary['total_devices']}",
            f"Total Checks: {summary['total_checks']}",
            f"Passed Checks: {summary['passed_checks']}",
            f"Failed Checks: {summary['failed_checks']}",
            "",
        ]

        for device_result in results:
            lines.append(f"Device: {device_result.get('hostname')}")
            lines.append(f"Management IP: {device_result.get('mgmt_ip')}")
            lines.append(f"Site: {device_result.get('site')}")
            lines.append(f"Role: {device_result.get('role')}")
            lines.append("-" * 25)

            for check_result in device_result.get("checks", []):
                lines.append(f"Check: {check_result.get('check')}")
                lines.append(f"Status: {check_result.get('status')}")
                lines.append(f"Details: {check_result.get('details')}")
                lines.append("")

            lines.append("")

        with open(self.text_report_file, "w", encoding="utf-8") as file:
            file.write("\n".join(lines))

    def _write_json_report(self, report_data):
        with open(self.json_report_file, "w", encoding="utf-8") as file:
            json.dump(report_data, file, indent=4)