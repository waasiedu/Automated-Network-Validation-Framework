import platform
import subprocess


def check_reachability(ip_address, count=3, timeout=3):
    if not ip_address:
        return {
            "check": "reachability",
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

        if result.returncode == 0:
            return {
                "check": "reachability",
                "status": "PASS",
                "details": f"{ip_address} is reachable",
            }

        return {
            "check": "reachability",
            "status": "FAIL",
            "details": f"{ip_address} is not reachable",
        }

    except Exception as error:
        return {
            "check": "reachability",
            "status": "FAIL",
            "details": str(error),
        }