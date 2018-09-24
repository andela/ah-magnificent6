import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict


class ArticleJSONRenderer(JSONRenderer):
    """JSONRenderClass for formatting Article model data into JSON."""

    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """Return data in json format."""

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


class BookmarkJSONRenderer(JSONRenderer):
    """JSONRenderClass for formatting Article model data into JSON."""

    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """Return data in json format."""
        error = data.get("errors", None)
        if error:
            """
            Let the default JSONRenderer handle rendering errors.
            """
            return super(BookmarkJSONRenderer, self).render(error)

        if type(data) == ReturnDict:
            # single bookmark
            return json.dumps({
                'Bookmark': data
            })
        else:
            # many bookmarks
            return json.dumps({
                'Bookmarks': data
            })
