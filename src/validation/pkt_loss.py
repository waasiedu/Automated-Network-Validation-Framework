import platform
import re
import subprocess


def check_packet_loss(ip_address, max_packet_loss_percent=0, count=5, timeout=3):
    if not ip_address:
        return {
            "check": "packet_loss",
            "status": "FAIL",
            "details": "No management IP address found",
        }

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", str(count), "-w", str(timeout * 1000), ip_address]
    else:
        command = ["ping", "-c", str(count), "-W", str(timeout), ip_address]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        output = result.stdout + result.stderr

        packet_loss = _extract_packet_loss(output)

        if packet_loss is None:
            return {
                "check": "packet_loss",
                "status": "FAIL",
                "details": "Unable to determine packet loss",
            }

        if packet_loss <= max_packet_loss_percent:
            return {
                "check": "packet_loss",
                "status": "PASS",
                "details": f"Packet loss {packet_loss:.2f}% is within threshold {max_packet_loss_percent}%",
                "value_percent": packet_loss,
                "threshold_percent": max_packet_loss_percent,
            }

        return {
            "check": "packet_loss",
            "status": "FAIL",
            "details": f"Packet loss {packet_loss:.2f}% exceeds threshold {max_packet_loss_percent}%",
            "value_percent": packet_loss,
            "threshold_percent": max_packet_loss_percent,
        }

    except Exception as error:
        return {
            "check": "packet_loss",
            "status": "FAIL",
            "details": str(error),
        }


def _extract_packet_loss(output):
    match = re.search(r"(\d+(?:\.\d+)?)% packet loss", output)
    if match:
        return float(match.group(1))

    match = re.search(r"\((\d+(?:\.\d+)?)% loss\)", output)
    if match:
        return float(match.group(1))

    return None