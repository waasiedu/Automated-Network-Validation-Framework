import platform
import re
import subprocess


def check_latency(ip_address, max_latency_ms=100, count=3, timeout=3):
    if not ip_address:
        return {
            "check": "latency",
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

        avg_latency = _extract_average_latency(output, system)

        if avg_latency is None:
            return {
                "check": "latency",
                "status": "FAIL",
                "details": "Unable to determine average latency",
            }

        if avg_latency <= max_latency_ms:
            return {
                "check": "latency",
                "status": "PASS",
                "details": f"Average latency {avg_latency:.2f} ms is within threshold {max_latency_ms} ms",
                "value_ms": avg_latency,
                "threshold_ms": max_latency_ms,
            }

        return {
            "check": "latency",
            "status": "FAIL",
            "details": f"Average latency {avg_latency:.2f} ms exceeds threshold {max_latency_ms} ms",
            "value_ms": avg_latency,
            "threshold_ms": max_latency_ms,
        }

    except Exception as error:
        return {
            "check": "latency",
            "status": "FAIL",
            "details": str(error),
        }


def _extract_average_latency(output, system):
    if system == "windows":
        match = re.search(r"Average = (\d+)ms", output)
        if match:
            return float(match.group(1))

    match = re.search(r"rtt min/avg/max/(?:mdev|stddev) = [\d.]+/([\d.]+)/", output)
    if match:
        return float(match.group(1))

    match = re.search(r"round-trip min/avg/max/(?:stddev|mdev) = [\d.]+/([\d.]+)/", output)
    if match:
        return float(match.group(1))

    return None