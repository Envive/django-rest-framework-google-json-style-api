from collections import OrderedDict


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

    errors = []
    for domain in data:
        error = data[domain]
        if domain == 'detail':
            domain = 'global'
            error = [error]
        for e in error:
            errors.append({
                'domain': domain,
                'reason': e.code,
                'message': str(e)
            })

    render_data = OrderedDict()
    render_data['error'] = OrderedDict([
        ('code', renderer_context.get('view').response.status_code),
        ('message', errors[0]['message']),
        ('errors', errors)
    ])

    return render_data
