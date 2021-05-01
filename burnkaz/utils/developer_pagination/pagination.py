import json

from django.core.paginator import InvalidPage
from django.http import JsonResponse
from rest_framework import status
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from collections import OrderedDict

# class DeveloperPagination(pagination.LimitOffsetPagination):
#     page_size = 5
#     # page_size_query_param = "page_size"
#     max_page_size = 10

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
            # msg = self.invalid_page_message.format(
            #     page_number=page_number, message=str(exc)
            # )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    # def paginate_queryset(self, queryset, request, view=None):
    #     """Checking NotFound exception"""
    #     try:
    #         return super(EmptyPagination, self).paginate_queryset(queryset, request, view=view)
    #     except NotFound:  # intercept NotFound exception
    #         return list()
    #
    # def get_paginated_response(self, data):
    #     """Avoid case when self does not have page properties for empty list"""
    #     if hasattr(self, 'page') and self.page is not None:
    #         return super(EmptyPagination, self).get_paginated_response(data)
    #     else:
    #         return Response(OrderedDict([
    #             ('count', None),
    #             ('next', None),
    #             ('previous', None),
    #             ('results', data)
    #         ]))