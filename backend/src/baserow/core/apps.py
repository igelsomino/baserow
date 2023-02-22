from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    name = "baserow.core"

    def ready(self):
        from baserow.core.action.registries import (
            action_scope_registry,
            action_type_registry,
        )
        from baserow.core.trash.registries import trash_item_type_registry
        from baserow.core.trash.trash_types import (
            ApplicationTrashableItemType,
            WorkspaceTrashableItemType,
        )

        trash_item_type_registry.register(WorkspaceTrashableItemType())
        trash_item_type_registry.register(ApplicationTrashableItemType())

        from baserow.core.permission_manager import (
            BasicPermissionManagerType,
            CorePermissionManagerType,
            StaffOnlyPermissionManagerType,
            StaffOnlySettingOperationPermissionManagerType,
            WorkspaceMemberOnlyPermissionManagerType,
        )
        from baserow.core.registries import (
            object_scope_type_registry,
            operation_type_registry,
            permission_manager_type_registry,
        )

        permission_manager_type_registry.register(CorePermissionManagerType())
        permission_manager_type_registry.register(StaffOnlyPermissionManagerType())
        permission_manager_type_registry.register(BasicPermissionManagerType())
        permission_manager_type_registry.register(
            WorkspaceMemberOnlyPermissionManagerType()
        )
        permission_manager_type_registry.register(
            StaffOnlySettingOperationPermissionManagerType()
        )

        from .object_scopes import (
            ApplicationObjectScopeType,
            CoreObjectScopeType,
            WorkspaceInvitationObjectScopeType,
            WorkspaceObjectScopeType,
            WorkspaceUserObjectScopeType,
        )
        from .snapshots.object_scopes import SnapshotObjectScopeType

        object_scope_type_registry.register(CoreObjectScopeType())
        object_scope_type_registry.register(ApplicationObjectScopeType())
        object_scope_type_registry.register(WorkspaceObjectScopeType())
        object_scope_type_registry.register(WorkspaceInvitationObjectScopeType())
        object_scope_type_registry.register(SnapshotObjectScopeType())
        object_scope_type_registry.register(WorkspaceUserObjectScopeType())

        from baserow.core.registries import subject_type_registry

        from .subjects import AnonymousUserSubjectType, UserSubjectType

        subject_type_registry.register(UserSubjectType())
        subject_type_registry.register(AnonymousUserSubjectType())

        from .operations import (
            CreateApplicationsWorkspaceOperationType,
            CreateInvitationsWorkspaceOperationType,
            CreateWorkspaceOperationType,
            DeleteApplicationOperationType,
            DeleteWorkspaceInvitationOperationType,
            DeleteWorkspaceOperationType,
            DeleteWorkspaceUserOperationType,
            DuplicateApplicationOperationType,
            ListApplicationsWorkspaceOperationType,
            ListInvitationsWorkspaceOperationType,
            ListWorkspacesOperationType,
            ListWorkspaceUsersWorkspaceOperationType,
            OrderApplicationsOperationType,
            ReadApplicationOperationType,
            ReadInvitationWorkspaceOperationType,
            ReadWorkspaceOperationType,
            RestoreApplicationOperationType,
            RestoreWorkspaceOperationType,
            UpdateApplicationOperationType,
            UpdateSettingsOperationType,
            UpdateWorkspaceInvitationType,
            UpdateWorkspaceOperationType,
            UpdateWorkspaceUserOperationType,
        )
        from .snapshots.operations import (
            CreateSnapshotApplicationOperationType,
            DeleteApplicationSnapshotOperationType,
            ListSnapshotsApplicationOperationType,
            RestoreApplicationSnapshotOperationType,
        )
        from .trash.operations import (
            EmptyApplicationTrashOperationType,
            EmptyWorkspaceTrashOperationType,
            ReadApplicationTrashOperationType,
            ReadWorkspaceTrashOperationType,
        )

        operation_type_registry.register(CreateApplicationsWorkspaceOperationType())
        operation_type_registry.register(CreateWorkspaceOperationType())
        operation_type_registry.register(CreateInvitationsWorkspaceOperationType())
        operation_type_registry.register(DeleteWorkspaceInvitationOperationType())
        operation_type_registry.register(DeleteWorkspaceOperationType())
        operation_type_registry.register(ListApplicationsWorkspaceOperationType())
        operation_type_registry.register(ListInvitationsWorkspaceOperationType())
        operation_type_registry.register(ReadInvitationWorkspaceOperationType())
        operation_type_registry.register(ListWorkspacesOperationType())
        operation_type_registry.register(UpdateWorkspaceInvitationType())
        operation_type_registry.register(ReadWorkspaceOperationType())
        operation_type_registry.register(UpdateWorkspaceOperationType())
        operation_type_registry.register(ListWorkspaceUsersWorkspaceOperationType())
        operation_type_registry.register(OrderApplicationsOperationType())
        operation_type_registry.register(UpdateWorkspaceUserOperationType())
        operation_type_registry.register(DeleteWorkspaceUserOperationType())
        operation_type_registry.register(UpdateApplicationOperationType())
        operation_type_registry.register(DuplicateApplicationOperationType())
        operation_type_registry.register(DeleteApplicationOperationType())
        operation_type_registry.register(UpdateSettingsOperationType())
        operation_type_registry.register(CreateSnapshotApplicationOperationType())
        operation_type_registry.register(DeleteApplicationSnapshotOperationType())
        operation_type_registry.register(ListSnapshotsApplicationOperationType())
        operation_type_registry.register(RestoreApplicationSnapshotOperationType())
        operation_type_registry.register(ReadWorkspaceTrashOperationType())
        operation_type_registry.register(ReadApplicationTrashOperationType())
        operation_type_registry.register(EmptyApplicationTrashOperationType())
        operation_type_registry.register(EmptyWorkspaceTrashOperationType())
        operation_type_registry.register(RestoreApplicationOperationType())
        operation_type_registry.register(RestoreWorkspaceOperationType())
        operation_type_registry.register(ReadApplicationOperationType())

        from baserow.core.actions import (
            AcceptWorkspaceInvitationActionType,
            CreateApplicationActionType,
            CreateWorkspaceActionType,
            CreateWorkspaceInvitationActionType,
            DeleteApplicationActionType,
            DeleteWorkspaceActionType,
            DeleteWorkspaceInvitationActionType,
            DuplicateApplicationActionType,
            InstallTemplateActionType,
            LeaveWorkspaceActionType,
            OrderApplicationsActionType,
            OrderWorkspacesActionType,
            RejectWorkspaceInvitationActionType,
            UpdateApplicationActionType,
            UpdateWorkspaceActionType,
            UpdateWorkspaceInvitationActionType,
        )

        action_type_registry.register(CreateWorkspaceActionType())
        action_type_registry.register(DeleteWorkspaceActionType())
        action_type_registry.register(UpdateWorkspaceActionType())
        action_type_registry.register(OrderWorkspacesActionType())
        action_type_registry.register(CreateApplicationActionType())
        action_type_registry.register(UpdateApplicationActionType())
        action_type_registry.register(DeleteApplicationActionType())
        action_type_registry.register(OrderApplicationsActionType())
        action_type_registry.register(DuplicateApplicationActionType())
        action_type_registry.register(InstallTemplateActionType())
        action_type_registry.register(CreateWorkspaceInvitationActionType())
        action_type_registry.register(DeleteWorkspaceInvitationActionType())
        action_type_registry.register(AcceptWorkspaceInvitationActionType())
        action_type_registry.register(RejectWorkspaceInvitationActionType())
        action_type_registry.register(UpdateWorkspaceInvitationActionType())
        action_type_registry.register(LeaveWorkspaceActionType())

        from baserow.core.snapshots.actions import (
            CreateSnapshotActionType,
            DeleteSnapshotActionType,
            RestoreSnapshotActionType,
        )

        action_type_registry.register(CreateSnapshotActionType())
        action_type_registry.register(DeleteSnapshotActionType())
        action_type_registry.register(RestoreSnapshotActionType())

        from baserow.core.trash.actions import (
            EmptyTrashActionType,
            RestoreFromTrashActionType,
        )

        action_type_registry.register(EmptyTrashActionType())
        action_type_registry.register(RestoreFromTrashActionType())

        from baserow.core.user.actions import (
            CancelUserDeletionActionType,
            ChangeUserPasswordActionType,
            CreateUserActionType,
            ResetUserPasswordActionType,
            ScheduleUserDeletionActionType,
            SendResetUserPasswordActionType,
            SignInUserActionType,
            UpdateUserActionType,
        )

        action_type_registry.register(CreateUserActionType())
        action_type_registry.register(UpdateUserActionType())
        action_type_registry.register(ScheduleUserDeletionActionType())
        action_type_registry.register(CancelUserDeletionActionType())
        action_type_registry.register(SignInUserActionType())
        action_type_registry.register(ChangeUserPasswordActionType())
        action_type_registry.register(SendResetUserPasswordActionType())
        action_type_registry.register(ResetUserPasswordActionType())

        from baserow.core.action.scopes import (
            ApplicationActionScopeType,
            RootActionScopeType,
            WorkspaceActionScopeType,
        )

        action_scope_registry.register(RootActionScopeType())
        action_scope_registry.register(WorkspaceActionScopeType())
        action_scope_registry.register(ApplicationActionScopeType())

        from baserow.core.jobs.registries import job_type_registry

        from .job_types import DuplicateApplicationJobType, InstallTemplateJobType
        from .snapshots.job_types import CreateSnapshotJobType, RestoreSnapshotJobType

        job_type_registry.register(DuplicateApplicationJobType())
        job_type_registry.register(InstallTemplateJobType())
        job_type_registry.register(CreateSnapshotJobType())
        job_type_registry.register(RestoreSnapshotJobType())

        from baserow.api.user.registries import user_data_registry
        from baserow.api.user.user_data_types import GlobalPermissionsDataType

        user_data_registry.register(GlobalPermissionsDataType())

        from baserow.core.auth_provider.auth_provider_types import (
            PasswordAuthProviderType,
        )
        from baserow.core.registries import auth_provider_type_registry

        auth_provider_type_registry.register(PasswordAuthProviderType())

        # Clear the key after migration so we will trigger a new template sync.
        post_migrate.connect(start_sync_templates_task_after_migrate, sender=self)
        # Create all operations from registry
        post_migrate.connect(sync_operations_after_migrate, sender=self)


# noinspection PyPep8Naming
def start_sync_templates_task_after_migrate(sender, **kwargs):
    from baserow.core.tasks import sync_templates_task

    if settings.BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION and not settings.TESTS:
        print(
            "Submitting the sync templates task to run asynchronously in "
            "celery after the migration..."
        )
        sync_templates_task.delay()


def sync_operations_after_migrate(sender, **kwargs):

    apps = kwargs.get("apps", None)

    if apps is not None:
        try:
            Operation = apps.get_model("core", "Operation")
        except LookupError:
            print("Skipping operation creation as Operation model does not exist.")
        else:
            from baserow.core.registries import operation_type_registry

            print("Creating all operations...")
            all_operation_types = [
                Operation(name=o.type) for o in operation_type_registry.get_all()
            ]
            Operation.objects.bulk_create(all_operation_types, ignore_conflicts=True)
