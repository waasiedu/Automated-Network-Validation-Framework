import yaml
from ping_check import check_reachability
from latency_check import measure_latency
from packet_loss_check import measure_packet_loss

CONFIG_FILE = "config/topology.yaml"

def load_topology():
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)["nodes"]

def run_validation():
    nodes = load_topology()
    results = []

    for node in nodes:
        name = node["name"]
        ip = node["ip"]

        reachable = check_reachability(ip)
        latency = measure_latency(ip) if reachable else None
        loss = measure_packet_loss(ip) if reachable else None

        results.append({
            "node": name,
            "ip": ip,
            "reachable": reachable,
            "latency_ms": latency,
            "packet_loss_pct": loss
        })

    return results

def print_report(results):
    print("Network Validation Report")
    print("=" * 30)

    for r in results:
        print(f"Node: {r['node']} ({r['ip']})")
        print(f"  Reachable: {r['reachable']}")
        print(f"  Avg Latency (ms): {r['latency_ms']}")
        print(f"  Packet Loss (%): {r['packet_loss_pct']}")
        print("-" * 30)

if __name__ == "__main__":
    report = run_validation()
    print_report(report)
