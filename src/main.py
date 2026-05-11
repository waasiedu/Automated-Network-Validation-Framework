import argparse

from src.reporting.report_writer import ReportWriter
from src.sources.netbox_source import NetBoxSource
from src.sources.validation_policy import ValidationPolicy
from src.sources.yaml_source import YAMLSource
from src.validation.latency import check_latency
from src.validation.pkt_loss import check_packet_loss
from src.validation.reachability import check_reachability


class ValidationEngine:
    def __init__(self, source, policy):
        self.source = source
        self.policy = policy

    def run(self):
        devices = self.source.get_devices()
        checks = self.policy.get_validation_checks()

        enabled_checks = {
            check.get("name"): check
            for check in checks
            if check.get("enabled", True)
        }

        results = []

        for device in devices:
            hostname = device.get("hostname") or device.get("name")
            mgmt_ip = device.get("mgmt_ip")

            device_result = {
                "hostname": hostname,
                "mgmt_ip": mgmt_ip,
                "site": device.get("site"),
                "role": device.get("role"),
                "platform": device.get("platform"),
                "checks": [],
            }

            if "reachability" in enabled_checks:
                device_result["checks"].append(
                    check_reachability(mgmt_ip)
                )

            if "latency" in enabled_checks:
                latency_config = enabled_checks["latency"]
                max_latency_ms = latency_config.get("max_latency_ms", 100)

                device_result["checks"].append(
                    check_latency(
                        mgmt_ip,
                        max_latency_ms=max_latency_ms,
                    )
                )

            if "packet_loss" in enabled_checks:
                packet_loss_config = enabled_checks["packet_loss"]
                max_packet_loss_percent = packet_loss_config.get(
                    "max_packet_loss_percent",
                    0,
                )

                device_result["checks"].append(
                    check_packet_loss(
                        mgmt_ip,
                        max_packet_loss_percent=max_packet_loss_percent,
                    )
                )

            results.append(device_result)

        return results


def get_source(source_type):
    if source_type == "yaml":
        return YAMLSource()

    if source_type == "netbox":
        return NetBoxSource()

    raise ValueError(f"Unsupported source type: {source_type}")


def main():
    parser = argparse.ArgumentParser(
        description="Automated Network Validation Framework"
    )

    parser.add_argument(
        "--source",
        choices=["yaml", "netbox"],
        default="yaml",
        help="Source of truth to use for inventory",
    )

    args = parser.parse_args()

    source = get_source(args.source)
    policy = ValidationPolicy()

    engine = ValidationEngine(source, policy)
    results = engine.run()

    writer = ReportWriter()
    report_paths = writer.write_reports(results)

    print("Validation completed.")
    print(f"Text report: {report_paths['text_report']}")
    print(f"JSON report: {report_paths['json_report']}")


if __name__ == "__main__":
    main()