import os
from pathlib import Path

import pynetbox
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    netbox_url = os.getenv("NETBOX_URL")
    netbox_token = os.getenv("NETBOX_TOKEN")

    if not netbox_url:
        raise ValueError("NETBOX_URL is required")

    if not netbox_token:
        raise ValueError("NETBOX_TOKEN is required")

    nb = pynetbox.api(netbox_url, token=netbox_token)

    print("\nNetBox Sites")
    print("-" * 40)
    for site in nb.dcim.sites.all():
        print(f"{site.name:20} slug={site.slug}")

    print("\nNetBox Devices")
    print("-" * 40)
    for device in nb.dcim.devices.all():
        site = device.site.name if device.site else "N/A"
        role = device.role.name if device.role else "N/A"
        platform = device.platform.name if device.platform else "N/A"
        primary_ip = device.primary_ip4.address if device.primary_ip4 else "N/A"

        print(
            f"{device.name:20} "
            f"site={site:12} "
            f"role={role:15} "
            f"platform={platform:10} "
            f"primary_ip={primary_ip}"
        )

    print("\nNetBox Interfaces")
    print("-" * 40)
    for interface in nb.dcim.interfaces.all():
        device_name = interface.device.name if interface.device else "N/A"
        print(
            f"{device_name:20} "
            f"interface={interface.name:15} "
            f"type={interface.type.value if interface.type else 'N/A'}"
        )

    print("\nNetBox IP Addresses")
    print("-" * 40)
    for ip in nb.ipam.ip_addresses.all():
        assigned_object = ip.assigned_object
        assigned_to = assigned_object.display if assigned_object else "N/A"

        print(f"{ip.address:20} assigned_to={assigned_to}")


if __name__ == "__main__":
    main()