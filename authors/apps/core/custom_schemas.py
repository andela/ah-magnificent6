import coreapi
from rest_framework.schemas import AutoSchema
import coreschema

class SearchFilterSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        """ Overide get_manual_fields to add extra fields 
            to get method schema to accomodate filter queries 
        """
        extra_fields = []
        if method=='GET':
            # Checks if method is get
            extra_fields = [
                # Adds extra fields
                coreapi.Field(
                    "author",
                    description="Filter by author",
                    required=False,
                    location="query",
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "title",
                    description="Filter by title",
                    required=False,
                    location="query",
                    schema=coreschema.String()
                ),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields