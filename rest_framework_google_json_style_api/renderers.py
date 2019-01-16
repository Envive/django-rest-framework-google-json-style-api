from collections import OrderedDict

from django_rest_framework_camel_case.util import camelize

from rest_framework_google_json_style_api.settings import api_settings


class JSONRenderer(api_settings.RENDERER_CLASS):
    def render(self, data, *args, **kwargs):
        media_type, renderer_context = args
        renderer_context = renderer_context or {}
        google_style_params = renderer_context.get('kwargs')
        google_style_params.update(
            renderer_context.get('request').query_params.items()
        )

        if data and 'results' in data:
            # Pagination
            data['items'] = data['results']
            data.pop('results', None)
            serialize_data = data
        else:
            serialize_data = {
                'items': data if type(data) == list else [data]
            }

        render_data = OrderedDict()
        render_data['method'] = renderer_context.get('view').action
        render_data['params'] = google_style_params
        render_data['data'] = serialize_data

        if api_settings.CAMELIZE:
            render_data = camelize(render_data)

        return super(JSONRenderer, self).render(render_data, *args, **kwargs)
