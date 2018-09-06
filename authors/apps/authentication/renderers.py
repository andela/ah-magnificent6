import json

from rest_framework.renderers import JSONRenderer
from .backends import generate_jwt_token
from .models import User



class UserJSONRenderer(JSONRenderer):
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
        try:
            """
            Checks whether the user is active and returns a message
            incase the user is not active.
            If the user is active, then it will pass.
            """
            confirm_user = data['email']
            user = User.objects.get(email=data['email'])
            if user.is_active is False:
                return json.dumps({
                    "Message":
                    "Account is not active. If registering, "
                    "kindly click the link sent to your email to "
                    "complete registration."
                    })
        except KeyError:
            pass

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'user': data
        })
