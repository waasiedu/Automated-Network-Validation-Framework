import subprocess

def check_reachability(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "3", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False
