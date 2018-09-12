import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict


class ArticleJSONRenderer(JSONRenderer):
    """JSONRenderClass for formating Article model data into JSON."""

    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Return data in json format.

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
            return super(ArticleJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            # single article
            return json.dumps({
                'Article': data
            })
        else:
            # many articles
            return json.dumps({
                'Articles': data
            })
