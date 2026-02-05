import subprocess
import re

def measure_latency(ip):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "5", ip],
            stderr=subprocess.DEVNULL
        ).decode()

        match = re.search(r"avg = ([0-9.]+)", output)
        if match:
            return float(match.group(1))
    except Exception:
        pass

    return None
