import traceback
import csv
from datetime import datetime
import json
import pytz

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.utils.decorators import method_decorator

from zelthy.core.api import get_api_response, ZelthyGenericPlatformAPIView
from zelthy.core.api.utils import ZelthyAPIPagination
from zelthy.core.permissions import IsSuperAdminPlatformUser
from zelthy.core.utils import get_search_columns
from zelthy.apps.shared.tenancy.models import TenantModel
from zelthy.apps.auditlog.models import LogEntry
from zelthy.core.common_utils import set_app_schema_path

from .serializers import AuditLogSerializerModel


@method_decorator(set_app_schema_path, name="dispatch")
class AuditLogViewAPIV1(ZelthyGenericPlatformAPIView, ZelthyAPIPagination):
    permission_classes = (IsSuperAdminPlatformUser,)
    pagination_class = ZelthyAPIPagination

    def process_timestamp(self, timestamp, timezone):
        try:
            ts = json.loads(timestamp)
            tz = pytz.timezone(timezone)
            ts["start"] = tz.localize(
                datetime.strptime(ts["start"] + "-" + "00:00", "%Y-%m-%d-%H:%M"),
                is_dst=None,
            )
            ts["end"] = tz.localize(
                datetime.strptime(ts["end"] + "-" + "23:59", "%Y-%m-%d-%H:%M"),
                is_dst=None,
            )
            return ts
        except Exception:
            return None

    def process_id(self, id):
        try:
            return int(id)
        except ValueError:
            return None

    def get_queryset(self, search, tenant, columns={}):

        field_name_query_mapping = {
            "tenant_actor": "tenant_actor__name__icontains",
            "platform_actor": "platform_actor__name__icontains",
            "object_id": "object_id",
            "id": "id",
            "object_repr": "object_repr__icontains",
            "changes": "changes__icontains",
            "object_uuid": "object_ref__object_uuid__icontains",
        }
        search_filters = {
            "id": self.process_id,
            "object_id": self.process_id,
            "timestamp": self.process_timestamp,
        }
        records = LogEntry.objects.all().order_by("-id")
        if search == "" and columns == {}:
            return records
        filters = Q()
        for field_name, query in field_name_query_mapping.items():
            if search:
                if search_filters.get(field_name, None):
                    filters |= Q(**{query: search_filters[field_name](search)})
                else:
                    filters |= Q(**{query: search})
        records = records.filter(filters).distinct()
        if columns.get("timestamp"):
            processed = self.process_timestamp(
                columns.get("timestamp"), tenant.timezone
            )
            if processed is not None:
                records = records.filter(
                    timestamp__gte=processed["start"], timestamp__lte=processed["end"]
                )
        if columns.get("action"):
            records = records.filter(action=columns.get("action"))
        if columns.get("object_type"):
            records = records.filter(
                content_type=ContentType.objects.get(id=columns.get("object_type"))
            )
        return records

    def get_dropdown_options(self):
        options = {}
        options["action"] = [
            {
                "id": "0",
                "label": "Create",
            },
            {
                "id": "1",
                "label": "Update",
            },
            {
                "id": "2",
                "label": "Delete",
            },
            {
                "id": "3",
                "label": "Access",
            },
        ]
        options["object_type"] = []
        object_types = list(
            LogEntry.objects.all()
            .values_list("content_type_id", "content_type__model")
            .order_by("content_type__model")
            .distinct()
        )
        for object_type in object_types:
            options["object_type"].append(
                {
                    "id": object_type[0],
                    "label": object_type[1],
                }
            )
        return options

    def get(self, request, *args, **kwargs):
        try:
            app_uuid = kwargs.get("app_uuid")
            tenant = TenantModel.objects.get(uuid=app_uuid)
            include_dropdown_options = request.GET.get("include_dropdown_options")
            search = request.GET.get("search", None)
            columns = get_search_columns(request)
            audit_logs = self.get_queryset(search, tenant, columns)
            paginated_audit_logs = self.paginate_queryset(
                audit_logs, request, view=self
            )
            serializer = AuditLogSerializerModel(
                paginated_audit_logs, many=True, context={"tenant": tenant}
            )
            auditlogs = self.get_paginated_response_data(serializer.data)
            success = True
            response = {
                "audit_logs": auditlogs,
                "message": "Audit logs fetched successfully",
            }
            if include_dropdown_options:
                response["dropdown_options"] = self.get_dropdown_options()
            status = 200
        except Exception as e:
            traceback.print_exc()
            success = False
            response = {"message": str(e)}
            status = 500
        return get_api_response(success, response, status)
