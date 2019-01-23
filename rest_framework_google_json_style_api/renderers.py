from collections import OrderedDict

from django_rest_framework_camel_case.util import camelize

from rest_framework_google_json_style_api.settings import api_settings

from . import utils


class JSONRenderer(api_settings.RENDERER_CLASS):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}

        # If this is an error response, skip the rest.
        if utils.is_error_response(renderer_context):
            return self.render_errors(data, accepted_media_type, renderer_context)

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
            if not data:
                serialize_data = {'items': []}
            elif issubclass(type(data), list):
                serialize_data = {'items': data}
            else:
                serialize_data = {'items': [data]}

        render_data = OrderedDict()
        render_data['method'] = renderer_context.get('view').action
        render_data['params'] = google_style_params
        render_data['data'] = serialize_data

        if api_settings.CAMELIZE:
            render_data = camelize(render_data)
        return super(JSONRenderer, self).render(render_data, accepted_media_type, renderer_context)

    def render_errors(self, data, accepted_media_type=None, renderer_context=None):
        render_data = utils.format_errors(data, accepted_media_type, renderer_context)
        if api_settings.CAMELIZE:
            render_data = camelize(render_data)
        return super(JSONRenderer, self).render(render_data, accepted_media_type, renderer_context)
