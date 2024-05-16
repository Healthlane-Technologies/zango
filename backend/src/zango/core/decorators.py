import ipaddress

from django.conf import settings
from django.http import Http404
from ipware.ip import get_client_ip


def internal_access_only(f):
    def decorate_view(request, *args, **kwargs):
        client_ip, is_routable = get_client_ip(request)
        allowed_ips = [ipaddress.ip_network(ip) for ip in settings.INTERNAL_IPS]
        if settings.ENV in ["staging", "prod"]:
            # Check if the client's IP is not in the allowed IPs
            if not any(ipaddress.ip_address(client_ip) in ip for ip in allowed_ips):
                # Raise a 404 error if the condition is met
                raise Http404
        return f(request, *args, **kwargs)

    return decorate_view
