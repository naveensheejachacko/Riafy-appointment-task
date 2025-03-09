from django.conf import settings

def api_base_url(request):
    """
    Makes API_BASE_URL available in all templates.
    Usage in templates: {{ API_BASE_URL }}
    """
    return {'API_BASE_URL': settings.API_BASE_URL}
