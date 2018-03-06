from functools import partial

from django.conf import settings
from django.shortcuts import render
from ocflib.lab.inventory import get_connection
from ocflib.lab.inventory import get_devices

get_connection = partial(
    get_connection,
    user=settings.OCFINVENTORY_USER,
    password=settings.OCFINVENTORY_PASSWORD,
    db=settings.OCFINVENTORY_DB,
)


def hardware(request):
    return render(request, 'stats/inventory.html', {'title': 'Lab Hardware Inventory', 'devices': get_devices()},)
