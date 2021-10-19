import datetime

import rest_framework.exceptions

from rest_framework.filters import SearchFilter, BaseFilterBackend

from django_filters.rest_framework import DjangoFilterBackend


class SearchNewsPostFilter(SearchFilter):
    pass


class DjangoFilterBackendCustom(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # print(request.query_params)

        created_date = request.query_params.get("created_date", None)
        year_date = request.query_params.get("year", None)
        # print(request.query_params, created_date)
        query = super(DjangoFilterBackendCustom, self).filter_queryset(request, queryset, view)
        # print(query.query)
        try:
            if created_date:
                date = datetime.datetime.strptime(created_date, "%Y-%m-%d")
                querysets = query.filter(created_date__date__gte=date)
                # print(querysets.query)
                return querysets
        except:
            raise rest_framework.exceptions.ValidationError(
                {"created_date": "Định dạng ngày tháng năm không đúng, vi dụ: yyyy-MM-dd"})

        if year_date:
            try:
                querysets = query.filter(created_date__year=year_date or 0)
                return querysets
            except:
                raise rest_framework.exceptions.ValidationError(
                    {"year": "Định dạng năm không hợp lệ, year là một số nguyên vd: " + str(
                        datetime.datetime.now().year)})

        return query

    def get_filterset_kwargs(self, request, queryset, view):
        data = request.query_params.copy()
        data.pop("created_date", None)
        data.pop("year", None)
        return {
            'data': data,
            'queryset': queryset,
            'request': request,
        }
