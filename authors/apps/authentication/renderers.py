import json

from rest_framework.renderers import JSONRenderer
from .backends import generate_jwt_token
from .models import User



class UserJSONRenderer(JSONRenderer):
    """
    Renderer which serializes data to JSON.
    """
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        If the view throws an error (such as the user can't be authenticated
        or something similar), `data` will contain an `errors` key. We want
        the default JSONRenderer to handle rendering errors, so we need to
        check for this case.
        """
        errors = data.get('errors', None)

        if errors:
            """
            As mentioned about, we will let the default JSONRenderer handle
            rendering errors.
            """

            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.

            return super(UserJSONRenderer, self).render(data)

        return json.dumps({
            'response': data
        })
