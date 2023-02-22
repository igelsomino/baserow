from django.utils import timezone

from baserow.core.models import Workspace
from baserow.core.usage.registries import workspace_storage_usage_item_registry
from baserow.core.utils import grouper


class UsageHandler:
    @classmethod
    def calculate_storage_usage(cls) -> int:
        """
        Calculates the storage usage of every workspace.
        :return: The amount of workspaces that have been updated.
        """

        # Item types might need to register some plpgsql functions
        # to speedup the calculations.
        for item in workspace_storage_usage_item_registry.get_all():
            if hasattr(item, "register_plpgsql_functions"):
                item.register_plpgsql_functions()

        count, chunk_size = 0, 256
        workspaces_queryset = Workspace.objects.filter(template__isnull=True).iterator(
            chunk_size=chunk_size
        )

        for workspaces in grouper(chunk_size, workspaces_queryset):
            now = timezone.now()
            for workspace in workspaces:
                usage_in_bytes = 0
                for item in workspace_storage_usage_item_registry.get_all():
                    usage_in_bytes += item.calculate_storage_usage(workspace.id)

                workspace.storage_usage = usage_in_bytes / (1024 * 1024)  # in MB
                workspace.storage_usage_updated_at = now

            Workspace.objects.bulk_update(
                workspaces, ["storage_usage", "storage_usage_updated_at"]
            )
            count += len(workspaces)

        return count
