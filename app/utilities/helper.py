import environ
from django.conf import settings
import requests
from app.device.models import Device

# from .models import Device

env = environ.Env()
ROOT_DIR = getattr(settings, "BASE_DIR", None)

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

LIBRE_TOKEN = env("LIBRE_TOKEN", default=None)
LIBRE_URL = env("LIBRE_URL", default=None)


def create_device_from_api(device_id=int):
    url = LIBRE_URL + "api/v0/devices/" + device_id
    headers = {"X-Auth-Token": "%s" % LIBRE_TOKEN}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        device = Device()
        device.hostname = data["hostname"]
        device.ip = data["ip"]
        device.id = data["device_id"]
        device.snmpcommunity = data["snmpcommunity"]
        device.snmpversion = data["snmpversion"]
        device.save()
        print("Successfully saved", device.hostname)


def get_devices(request):
    # data = []
    url = LIBRE_URL + "api/v0/devices/"
    headers = {"X-Auth-Token": "%s" % LIBRE_TOKEN}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        devices = data["devices"]

        for device in devices:
            device_id = device["device_id"]
            if not Device.objects.filter(id=device_id).exists():
                create_device_from_api(device_id)


def get_device_detail_view(pk):
    url = LIBRE_URL + "api/v0/devices/" + str(pk)
    headers = {"X-Auth-Token": "%s" % LIBRE_TOKEN}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        response = r.json()
        if response["status"] == "ok":
            device_data = response["devices"]
            return device_data
    return {}
