import json
import traceback

from django.conf import settings
from django.utils.decorators import method_decorator

from zelthy.core.api import (
    get_api_response,
    ZelthyGenericPlatformAPIView,
)
from zelthy.apps.shared.tenancy.models import TenantModel
from zelthy.apps.shared.tenancy.utils import TIMEZONES, DATETIMEFORMAT
from zelthy.apps.permissions.models import PolicyModel, PermissionsModel
from zelthy.core.common_utils import set_app_schema_path
from zelthy.core.api.utils import ZelthyAPIPagination

from .serializers import PolicySerializer


@method_decorator(set_app_schema_path, name="dispatch")
class PolicyViewAPIV1(ZelthyGenericPlatformAPIView, ZelthyAPIPagination):
    pagination_class = ZelthyAPIPagination

    def get(self, request, *args, **kwargs):
        try:
            policies = PolicyModel.objects.all().order_by("-modified_at")

            paginated_roles = self.paginate_queryset(policies, request, view=self)
            serializer = PolicySerializer(paginated_roles, many=True)
            paginated_roles_data = self.get_paginated_response_data(serializer.data)

            success = True
            response = {
                "policies": paginated_roles_data,
                "message": "All policies fetched successfully",
            }
            status = 200
        except Exception as e:
            success = False
            response = {"message": str(e)}
            status = 500

        return get_api_response(success, response, status)

    def post(self, request, *args, **kwargs):
        data = request.data
        policy_serializer = PolicySerializer(data=data)
        if policy_serializer.is_valid():
            success = True
            status_code = 200
            policy = policy_serializer.save()
            result = {"message": "Policy Created Successfully", "policy_id": policy.id}
        else:
            success = False
            status_code = 400
            if policy_serializer.errors:
                error_messages = [
                    error[0] for field_name, error in policy_serializer.errors.items()
                ]
                error_message = ", ".join(error_messages)
            else:
                error_message = "Invalid data"

            result = {"message": error_message}

        return get_api_response(success, result, status_code)


@method_decorator(set_app_schema_path, name="dispatch")
class PolicyDetailViewAPIV1(ZelthyGenericPlatformAPIView):
    def get_obj(self, **kwargs):
        obj = PolicyModel.objects.get(id=kwargs.get("policy_id"))
        return obj

    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_obj(**kwargs)
            serializer = PolicySerializer(obj)
            success = True
            response = {"policy": serializer.data}
            status = 200
        except Exception as e:
            success = False
            response = {"message": str(e)}
            status = 500

        return get_api_response(success, response, status)

    def put(self, request, *args, **kwargs):
        try:
            obj = self.get_obj(**kwargs)
            serializer = PolicySerializer(instance=obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                success = True
                status_code = 200
                result = {
                    "message": "Policy Updated Successfully",
                    "policy_id": obj.id,
                }
            else:
                success = False
                status_code = 400
                if serializer.errors:
                    error_messages = [
                        error[0] for field_name, error in serializer.errors.items()
                    ]
                    error_message = ", ".join(error_messages)
                else:
                    error_message = "Invalid data"

                result = {"message": error_message}
        except Exception as e:
            success = False
            result = {"message": str(e)}
            status_code = 500

        return get_api_response(success, result, status_code)
