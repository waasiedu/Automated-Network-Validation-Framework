import os

import pynetbox

from src.sources.base import SourceOfTruth


class NetBoxSource(SourceOfTruth):
    def __init__(self, url=None, token=None):
        self.url = url or os.getenv("NETBOX_URL")
        self.token = token or os.getenv("NETBOX_TOKEN")

        if not self.url or not self.token:
            raise ValueError("NETBOX_URL and NETBOX_TOKEN must be set")

        self.nb = pynetbox.api(self.url, token=self.token)

    def get_sites(self):
        sites = []

        for site in self.nb.dcim.sites.all():
            sites.append(
                {
                    "name": site.name,
                    "slug": site.slug,
                    "region": site.region.name if site.region else None,
                    "description": site.description,
                }
            )

        return sites

    def get_devices(self):
        devices = []

        for device in self.nb.dcim.devices.all():
            primary_ip = None

            if device.primary_ip4:
                primary_ip = str(device.primary_ip4.address).split("/")[0]
            elif device.primary_ip6:
                primary_ip = str(device.primary_ip6.address).split("/")[0]

            devices.append(
                {
                    "hostname": device.name,
                    "site": device.site.name if device.site else None,
                    "role": device.role.name if device.role else None,
                    "platform": device.platform.name if device.platform else None,
                    "mgmt_ip": primary_ip,
                    "status": str(device.status) if device.status else None,
                }
            )

        return devices