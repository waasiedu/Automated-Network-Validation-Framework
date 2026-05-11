from src.engine.validation_engine import ValidationEngine


class FakeSource:
    def get_devices(self):
        return [
            {
                "hostname": "router1",
                "site": "dc1",
                "role": "edge-router",
                "platform": "cisco_ios",
                "mgmt_ip": "192.168.56.101",
            }
        ]


class FakePolicy:
    def get_validation_checks(self):
        return [
            {
                "name": "reachability",
                "enabled": True,
            }
        ]


def fake_reachability_check(ip_address):
    return {
        "check": "reachability",
        "status": "PASS",
        "details": f"{ip_address} is reachable",
    }


def test_validation_engine_runs_reachability_check(monkeypatch):
    monkeypatch.setattr(
        "src.engine.validation_engine.check_reachability",
        fake_reachability_check,
    )

    source = FakeSource()
    policy = FakePolicy()

    engine = ValidationEngine(source, policy)
    results = engine.run()

    assert len(results) == 1

    device_result = results[0]

    assert device_result["hostname"] == "router1"
    assert device_result["mgmt_ip"] == "192.168.56.101"
    assert len(device_result["checks"]) == 1

    check_result = device_result["checks"][0]

    assert check_result["check"] == "reachability"
    assert check_result["status"] == "PASS"