from django.shortcuts import render
from ocflib.lab.inventory import get_devices


def hardware(request):
    return render(request, 'stats/inventory.html', {'title': 'Lab Hardware Inventory', 'devices': get_devices()},)
