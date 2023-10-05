from django.core.management.base import BaseCommand, CommandError
import os
import shutil
from django.conf import settings
from django.db import connection
from zelthy.apps.shared.tenancy.models import TenantModel
from zelthy.apps.dynamic_models.workspace.base import Workspace

class Command(BaseCommand):
    help = 'Collects assets from the specified app, including plugins and copies into \
            the main django asset folder'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "workspace",
            help="The workspace name to be used.",
        )

    def copy_source_to_destination(self, source_dir, destination_dir):
        if os.path.exists(destination_dir):
            shutil.rmtree(destination_dir)
        os.makedirs(destination_dir)
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(destination_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)
        return



    def handle(self, *args, **options):
        wks_obj = TenantModel.objects.get(name=options['workspace']) 
        connection.set_tenant(wks_obj)
        ws = Workspace(wks_obj, None,  True)        
        destination_path = settings.STATICFILES_DIRS[0] + "/workspaces/%s"%(options['workspace'])
        ws_static_path= ws.path + "static"
        self.copy_source_to_destination(ws_static_path, destination_path)

        for plugin in ws.plugins:
            plugin_name = plugin['name']
            plugin_source_dir = ws.path + "plugins/%s/static"%(plugin_name)
            if os.path.exists(plugin_source_dir):
                plugin_destination_dir = destination_path + "/plugins/%s"%plugin_name
                self.copy_source_to_destination(plugin_source_dir, plugin_destination_dir)
        return