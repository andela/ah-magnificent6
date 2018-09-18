import json

from rest_framework.renderers import JSONRenderer


class NotificationJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Check for errors key in data
        """
        errors = data.get('errors', None)

        if errors:
            """
            We will let the default JSONRenderer handle
            rendering errors.
            """
            return super(NotificationJSONRenderer, self).render(data)

        # Finally, we can render our data under the "profile" namespace.
        return json.dumps({
            'notification': data
        })
