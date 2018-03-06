from functools import partial
from ipaddress import ip_address
from json import loads as json_load_string

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ocflib.infra.hosts import hosts_by_filter
from ocflib.infra.net import is_ocf_ip
from ocflib.lab.inventory import get_connection

from ocfweb.caching import cache

get_connection = partial(
    get_connection,
    user=settings.OCFINVENTORY_USER,
    password=settings.OCFINVENTORY_PASSWORD,
    db=settings.OCFINVENTORY_DB,
)


@require_POST
@csrf_exempt
def update_inventory(request):

    desktop_ip = request.META['REMOTE_ADDR']

    if not is_ocf_ip(ip_address(desktop_ip)):
        return HttpResponse('Not Authorized', status=401)

    try:
        hardware = json_load_string(request.body.decode('utf-8'))

        hostname = hardware['hostname']

        if not hostname == _get_hostname(desktop_ip):
            return HttpResponse('Not Authorized', status=401)

        if hostname == '' or hostname is None:
            raise ValueError('Invalid host "{}"'.format(hostname))

        for device in hardware['devices']:
            device_class = device['class']
            if device_class == '' or device_class is None:
                raise ValueError('Invalid device class "{}"'.format(device_class))

            device_merchant = device['merchant']
            if device_merchant == '' or device_merchant is None:
                raise ValueError('Invalid device merchant "{}"'.format(device_merchant))

            device_name = device['name']
            if device_name == '' or device_name is None:
                raise ValueError('Invalid device name "{}"'.format(device_name))

            _add_desktop_device(hostname, device_class, device_merchant, device_name)

        return HttpResponse(status=204)

    except ValueError as e:
        return HttpResponseBadRequest(e)


def _add_desktop_device(hostname, device_class, device_merchant, device_name):
    values = '("{hostname}", "{device_class}", "{device_merchant}", "{device_name}", NOW())'.format(
        hostname=hostname, device_class=device_class, device_merchant=device_merchant, device_name=device_name,
    )
    with get_connection() as c:
        c.execute('INSERT INTO `lab_inventory` VALUES' + values + 'ON DUPLICATE KEY UPDATE `last_seen`=NOW()')


@cache()
def _get_hostname(ip):
    return {e['ipHostNumber'][0]: e['cn'][0]
            for e in hosts_by_filter('(type=desktop)')}.get(ip)
