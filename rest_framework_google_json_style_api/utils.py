from collections import OrderedDict

import inflection
from rest_framework_google_json_style_api.settings import api_settings


def is_error_response(context):
    """
    Return boolen value of the view.
    """
    view = context.get('view')
    try:
        code = str(view.response.status_code)
    except (AttributeError, ValueError):
        pass
    else:
        if code.startswith('4') or code.startswith('5'):
            return True
    return False


def format_errors(data, accepted_media_type, renderer_context):
    """
    Return error json response.

    Follow the style at the link below:
    https://google.github.io/styleguide/jsoncstyleguide.xml?showone=error.message#error
    https://cloud.google.com/storage/docs/json_api/v1/status-codes

    {
        "error": {
            "code": 404,
            "message": "File Not Found",
            "errors": [{
                "domain": "calendar",
                "reason": "ResourceNotFoundException",
                "message": "File Not Found
            }]
        }
    }
    """
    def integrate_domains(domains):
        domains = filter(None, domains)
        if api_settings.CAMELIZE:
            domains = [inflection.camelize(domain, False) for domain in domains]
        return ".".join(domains)

    def process_errors(data, parent_domain=""):
        errors = []
        for domain in data:
            error = data[domain]
            if domain == 'detail':
                domain = 'global'
                error = [error]
            integrated_domain = integrate_domains([parent_domain, domain])
            for e in error:
                if isinstance(e, dict):
                    errors.extend(process_errors(e, integrated_domain))
                else:
                    errors.append({
                        'domain': integrated_domain,
                        'reason': e.code,
                        'message': str(e)
                    })
        return errors

    errors = process_errors(data)
    render_data = OrderedDict()
    render_data['error'] = OrderedDict([
        ('code', renderer_context.get('view').response.status_code),
        ('message', errors[0]['message']),
        ('errors', errors)
    ])

    return render_data
