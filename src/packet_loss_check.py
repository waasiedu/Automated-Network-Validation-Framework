import subprocess
import re

def measure_packet_loss(ip):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "10", ip],
            stderr=subprocess.DEVNULL
        ).decode()

        match = re.search(r"(\d+)% packet loss", output)
        if match:
            return int(match.group(1))
    except Exception:
        pass

    return None
