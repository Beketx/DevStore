import os

from django.core.paginator import InvalidPage
from rest_framework import pagination
from rest_framework.exceptions import ValidationError, NotFound
from datetime import datetime


class DeveloperPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            msg = {
                "count": 0,
                "results": []
            }
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)



MAX_FILE_SIZE = 1024000
ALLOWED_EXTENSIONS = ['.jpg', '.png']

def developer_photos_size(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f'max file size is: {MAX_FILE_SIZE}')

def developer_file_extension(value):
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if not ext.lower() in ALLOWED_EXTENSIONS:
            raise ValidationError(f'not allowed file value extension, valid extensions: {ALLOWED_EXTENSIONS}')

def developer_photos_path(instance, filename):
    user = instance.user
    date = datetime.today().strftime('%Y-%m-%d')
    return f'dev_profile_avatars/users/{user.id}/{str(date)}/{filename}'