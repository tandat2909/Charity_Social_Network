from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import OptionReport
from ..permission import PermissionUserReport
from ..serializers import OptionReportSerializer


class ReportViewSet(ListModelMixin, GenericViewSet):
    queryset = OptionReport.objects.all()
    serializer_class = OptionReportSerializer
    permission_classes = [PermissionUserReport]