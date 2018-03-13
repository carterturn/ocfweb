from ipaddress import ip_address
from json import loads as json_load_string

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ocflib.infra.hosts import hosts_by_filter
from ocflib.infra.net import is_ocf_ip
from ocflib.lab.inventory import add_host_inventory

from ocfweb.caching import cache


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

        add_host_inventory(hardware)

        return HttpResponse('')

    except ValueError as e:
        return HttpResponseBadRequest(e)


@cache()
def _get_hostname(ip):
    return {e['ipHostNumber'][0]: e['cn'][0]
            for e in hosts_by_filter('(type=desktop)')}.get(ip)
