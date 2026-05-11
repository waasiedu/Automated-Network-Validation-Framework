import os
import sys
from pathlib import Path

import yaml
import pynetbox
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_OF_TRUTH_DIR = PROJECT_ROOT / "source_of_truth"


def load_yaml_file(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data or {}


def slugify(value):
    return (
        value.strip()
        .lower()
        .replace(" ", "-")
        .replace("_", "-")
        .replace("/", "-")
    )


class NetBoxPopulator:
    def __init__(self, url, token):
        if not url:
            raise ValueError("NETBOX_URL is required")

        if not token:
            raise ValueError("NETBOX_TOKEN is required")

        self.nb = pynetbox.api(url, token=token)

    def get_or_create_site(self, site_data):
        name = site_data["name"]
        slug = site_data.get("slug") or slugify(name)

        existing = self.nb.dcim.sites.get(slug=slug)
        if existing:
            print(f"[EXISTS] site: {name}")
            return existing

        payload = {
            "name": name,
            "slug": slug,
            "description": site_data.get("description", ""),
        }

        site = self.nb.dcim.sites.create(payload)
        print(f"[CREATED] site: {name}")
        return site

    def get_or_create_manufacturer(self, name):
        if not name:
            name = "Generic"

        slug = slugify(name)

        existing = self.nb.dcim.manufacturers.get(slug=slug)
        if existing:
            print(f"[EXISTS] manufacturer: {name}")
            return existing

        manufacturer = self.nb.dcim.manufacturers.create({
            "name": name,
            "slug": slug,
        })

        print(f"[CREATED] manufacturer: {name}")
        return manufacturer

    def get_or_create_device_type(self, model, manufacturer):
        if not model:
            model = "Generic Device"

        slug = slugify(model)

        existing = self.nb.dcim.device_types.get(
            model=model,
            manufacturer_id=manufacturer.id,
        )

        if existing:
            print(f"[EXISTS] device type: {model}")
            return existing

        device_type = self.nb.dcim.device_types.create({
            "model": model,
            "slug": slug,
            "manufacturer": manufacturer.id,
        })

        print(f"[CREATED] device type: {model}")
        return device_type

    def get_or_create_device_role(self, name):
        if not name:
            name = "network-device"

        slug = slugify(name)

        existing = self.nb.dcim.device_roles.get(slug=slug)
        if existing:
            print(f"[EXISTS] device role: {name}")
            return existing

        role = self.nb.dcim.device_roles.create({
            "name": name,
            "slug": slug,
            "color": "2196f3",
        })

        print(f"[CREATED] device role: {name}")
        return role

    def get_or_create_platform(self, name):
        if not name:
            return None

        slug = slugify(name)

        existing = self.nb.dcim.platforms.get(slug=slug)
        if existing:
            print(f"[EXISTS] platform: {name}")
            return existing

        platform = self.nb.dcim.platforms.create({
            "name": name,
            "slug": slug,
        })

        print(f"[CREATED] platform: {name}")
        return platform

    def get_or_create_interface(self, device, name="mgmt0"):
        existing = self.nb.dcim.interfaces.get(
            device_id=device.id,
            name=name,
        )

        if existing:
            print(f"[EXISTS] interface: {device.name} {name}")
            return existing

        interface = self.nb.dcim.interfaces.create({
            "device": device.id,
            "name": name,
            "type": "virtual",
        })

        print(f"[CREATED] interface: {device.name} {name}")
        return interface

    def get_or_create_ip_address(self, address, interface):
        if not address:
            return None

        existing = self.nb.ipam.ip_addresses.get(address=address)
        if existing:
            print(f"[EXISTS] IP address: {address}")

            if not existing.assigned_object:
                existing.update({
                    "assigned_object_type": "dcim.interface",
                    "assigned_object_id": interface.id,
                })
                print(f"[UPDATED] assigned IP {address} to interface {interface.name}")

            return existing

        ip_address = self.nb.ipam.ip_addresses.create({
            "address": address,
            "assigned_object_type": "dcim.interface",
            "assigned_object_id": interface.id,
        })

        print(f"[CREATED] IP address: {address}")
        return ip_address

    def get_or_create_device(self, device_data):
        hostname = device_data["hostname"]

        site_name = device_data["site"]
        site = self.nb.dcim.sites.get(slug=slugify(site_name)) or self.nb.dcim.sites.get(name=site_name)

        if not site:
            raise ValueError(f"Site '{site_name}' does not exist in NetBox")

        manufacturer = self.get_or_create_manufacturer(
            device_data.get("manufacturer", "Generic")
        )

        device_type = self.get_or_create_device_type(
            device_data.get("device_type", "Generic Device"),
            manufacturer,
        )

        role = self.get_or_create_device_role(
            device_data.get("role", "network-device")
        )

        platform = self.get_or_create_platform(
            device_data.get("platform")
        )

        existing = self.nb.dcim.devices.get(name=hostname)

        payload = {
            "name": hostname,
            "site": site.id,
            "device_type": device_type.id,
            "role": role.id,
        }

        if platform:
            payload["platform"] = platform.id

        if existing:
            existing.update(payload)
            device = existing
            print(f"[UPDATED] device: {hostname}")
        else:
            device = self.nb.dcim.devices.create(payload)
            print(f"[CREATED] device: {hostname}")

        mgmt_ip = device_data.get("mgmt_ip")

        if mgmt_ip:
            mgmt_interface = self.get_or_create_interface(device, "mgmt0")
            ip_address = self.get_or_create_ip_address(mgmt_ip, mgmt_interface)

            if ip_address:
                device.update({
                    "primary_ip4": ip_address.id,
                })
                print(f"[UPDATED] primary IPv4 for {hostname}: {mgmt_ip}")

        return device

    def populate_sites(self, sites):
        for site in sites:
            self.get_or_create_site(site)

    def populate_devices(self, devices):
        for device in devices:
            self.get_or_create_device(device)


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    netbox_url = os.getenv("NETBOX_URL")
    netbox_token = os.getenv("NETBOX_TOKEN")

    sites_file = SOURCE_OF_TRUTH_DIR / "sites.yaml"
    devices_file = SOURCE_OF_TRUTH_DIR / "devices.yaml"

    sites_data = load_yaml_file(sites_file)
    devices_data = load_yaml_file(devices_file)

    sites = sites_data.get("sites", [])
    devices = devices_data.get("devices", [])

    if not sites:
        print("No sites found in source_of_truth/sites.yaml")
        sys.exit(1)

    if not devices:
        print("No devices found in source_of_truth/devices.yaml")
        sys.exit(1)

    populator = NetBoxPopulator(netbox_url, netbox_token)

    print("\nPopulating NetBox sites...")
    populator.populate_sites(sites)

    print("\nPopulating NetBox devices...")
    populator.populate_devices(devices)

    print("\nNetBox population completed successfully.")
    

if __name__ == "__main__":
    main()