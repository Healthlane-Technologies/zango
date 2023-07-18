from django.core.management.base import BaseCommand, CommandError, CommandParser
import os
import importlib
import sys
import inspect
from zelthy3.backend.apps.tenants.datamodel.models import DynamicTable
import traceback
from django.db import connection
from django.db import models
from django.db.models.base import ModelBase
from django_tenants.utils import get_tenant_model
from zelthy3.zelthy_preprocessor import ZimportStack, ZPreprocessor
from zelthy3.backend.apps.tenants.datamodel.models import SimpleMixim
from django.apps import apps

class Command(BaseCommand):
    help = "Performs the migration operation for the datamodels in the project"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("tenant_name", help="Name of the tenant")
        parser.add_argument("module_name", help="Name of the module containing the model")

    def handle(self, *args, **options):
        tenant_name = options["tenant_name"]
        tenant_model = get_tenant_model()
        env = tenant_model.objects.get(name=tenant_name)
        connection.set_tenant(env)
        with connection.cursor() as c:
            sys.path.append(os.getcwd())
            
            modules = os.listdir(f"./zelthy_apps/{tenant_name}")
            if options["module_name"]:
                modules = [options["module_name"]]
            
            for module in modules:

                ddms = {}
            
                with open(f"./zelthy_apps/{tenant_name}/{module}/models.py") as f:
                    content = f.read()
                    exec(content, globals())
                    for name, obj in globals().items():
                        if type(obj) == ModelBase and name not in ["ModelBase", "DynamicTable", "SimpleMixim"]:
                            obj.__module__ = f"zelthy_apps.{tenant_name}.{module}.models"
                            ddms[name] = obj

                for desc, dataclass in ddms.items():
                    field_specs = []
                    for field_name, specs in vars(dataclass).items():
                        if field_name == "one_to_one_1":
                            attrs = {}
                            field_type = "DataModelOneToOneField"
                            for field, val in vars(specs).items():
                                attrs[field] = val
                            field_spec = {
                                "field_name": field_name,
                                "attrs": attrs,
                                "field_type": field_type
                            }
                            field_specs.append(field_spec)
                        elif field_name == "foreign_key_1":
                            attrs = {}
                            field_type = "DataModelForeignKey"
                            for field, val in vars(specs).items():
                                attrs[field] = val
                            field_spec = {
                                "field_name": field_name,
                                "attrs": attrs,
                                "field_type": field_type
                            }
                            field_specs.append(field_spec)
                        elif field_name == "many_to_many_1":
                            attrs = {}
                            field_type = "DataModelManyToManyField"
                            for field, val in vars(specs).items():
                                attrs[field] = val
                            field_spec = {
                                "field_name": field_name,
                                "attrs": attrs,
                                "field_type": field_type
                            }
                            field_specs.append(field_spec)
                        elif field_name in ["name", "dota", "jame", "role"]:
                            attrs = {}
                            if vars(specs).get("field"):
                                field_type = str(vars(specs)["field"].__class__)
                                field_type = field_type[field_type.rfind(".") + 1:field_type.rfind("'")]
                                attrs = {}
                                for field, val in vars(vars(specs)["field"]).items():
                                    # if field != "_unique" or field != 'is_relation':
                                    #     if type(val) in [ int, bool, float, str, dict, None]:
                                    #         attrs[field] = val
                                    if field == "max_length" or field == "default":
                                        if type(val) in [ int, bool, float, str, dict, None]:
                                            attrs[field] = val
                            field_spec = {
                                "field_name": field_name,
                                "attrs": attrs,
                                "field_type": field_type
                            }
                            field_specs.append(field_spec)
                    model_name = "".join(desc)
                    print(field_specs)
                    obj = None
                    
                    try:
                        obj = DynamicTable.objects.get(label=desc)
                    except:
                        obj = DynamicTable(label=desc, description="", field_specs={})
                        obj.full_clean()
                        obj.save()
                    
                    obj.update_model_schema(field_specs, desc)
                    obj.migrate_schema()
