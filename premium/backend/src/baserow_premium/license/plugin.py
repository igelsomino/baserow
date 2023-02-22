import logging
from typing import Dict, Generator, Optional, Set

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

from baserow_premium.license.exceptions import InvalidLicenseError
from baserow_premium.license.models import License
from baserow_premium.license.registries import LicenseType

from baserow.core.models import Workspace

logger = logging.getLogger(__name__)
User = get_user_model()


class LicensePlugin:
    """
    A collection of methods used to query for what licenses a user has access to and
    hence which features they can use.
    """

    def user_has_feature(
        self,
        feature: str,
        user: AbstractUser,
        workspace: Workspace,
    ) -> bool:
        """
        Returns if the provided user has a feature enabled for a specific workspace from
        an active license or if they have that feature enabled instance wide and hence
        also for this workspace.

        :param feature: A string identifying a particular feature or set of features
            a license can grant a user.
        :param user: The user to check to see if they have a license active granting
            them the feature.
        :param workspace: The workspace to check to see if the user has the feature for.
        """

        return self.user_has_feature_instance_wide(feature, user) or (
            self._has_license_feature_only_for_specific_workspace(
                feature, user, workspace
            )
        )

    def instance_has_feature(
        self,
        feature: str,
    ) -> bool:
        """
        Checks if the Baserow instance has a particular feature granted by an active
        instance wide license.

        :param feature: The feature to check to see if active. Look for features.py
            files for these constant strings to use.
        :return: True if the feature is enabled globally for all users.
        """

        return any(
            feature in license_type.features
            for license_type in self.get_active_instance_wide_licenses(user=None)
        )

    def workspace_has_feature(self, feature: str, workspace: Workspace) -> bool:
        """
        Checks if the Baserow instance has a particular feature granted by an active
        instance wide license.

        :param feature: The feature to check to see if active. Look for features.py
            files for these constant strings to use.
        :param workspace: The workspace to get workspace wide features for.
        :return: True if the feature is enabled globally for all users.
        """

        return self.instance_has_feature(feature) or any(
            feature in license_type.features
            for license_type in self.get_active_workspace_licenses(workspace)
        )

    def user_has_feature_instance_wide(self, feature: str, user: AbstractUser) -> bool:
        """
        Returns if the provided user has a feature enabled for the entire site,
        and not only for one specific workspace from an active license.

        :param feature: A string identifying a particular feature or set of features
            a license can grant a user.
        :param user: The user to check to see if they have a license active granting
            them the feature.
        """

        return any(
            feature in license_type.features
            for license_type in self.get_active_instance_wide_licenses(user)
        )

    def _has_license_feature_only_for_specific_workspace(
        self, feature: str, user: AbstractUser, workspace: Workspace
    ) -> bool:
        """
        Returns if the provided user has a feature enabled for a specific workspace from
        an active license, but ignoring any instance-wide licenses they might have.

        :param feature: A string identifying a particular feature or set of features
            a license can grant a user.
        :param user: The user to check to see if they have a workspace level license
            active granting them the feature.
        :param workspace: The workspace to check to see if the user has the feature for.
        """

        return any(
            feature in license_type.features
            for license_type in self.get_active_specific_licenses_only_for_workspace(
                user, workspace
            )
        )

    def get_active_instance_wide_licenses(
        self, user: Optional[AbstractUser]
    ) -> Generator[LicenseType, None, None]:
        """
        For the provided user returns the active licenses they have instance wide.
        If no user is provided then returns any licenses that are globally active for
        every single user in the instance.

        :param user: The user to lookup active instance wide licenses for.
        """

        available_license_q = Q(cached_untrusted_instance_wide=True)
        if user is not None:
            available_license_q |= Q(users__user_id__in=[user.id])

        available_licenses = License.objects.filter(available_license_q).distinct()

        for available_license in available_licenses:
            try:
                if available_license.is_active:
                    yield available_license.license_type
            except InvalidLicenseError:
                pass

    def get_active_specific_licenses_only_for_workspace(
        self, user: AbstractUser, workspace: Workspace
    ) -> Generator[LicenseType, None, None]:
        """
        Generates all the licenses for a specific workspace that a user has. Should not
        return any instance-wide licenses the user has.

        Provided as an overridable hook incase querying for only one specific workspace
        can be optimized. By default just defers to the `get_per_workspace_licenses`
        function.

        :param user: The user to get active licenses in the workspace for.
        :param workspace: The workspace to check to see any specific active licenses are
            enabled for.
        :return: A generator which produces the license types that the user has enabled
            for the workspace.
        """

        per_workspace_licenses = self.get_active_per_workspace_licenses(user)
        for active_license in per_workspace_licenses.get(workspace.id, set()):
            yield active_license

    def get_active_per_workspace_licenses(
        self, user: AbstractUser
    ) -> Dict[int, Set[LicenseType]]:
        """
        For the provided user returns the active licenses they have active per
        workspace. Does not take into account any instance wide licenses the user
        might have and only active licenses for specific workspaces.

        :param user: The user to lookup active per workspace licenses for.
        """

        return {}

    def get_active_workspace_licenses(
        self,
        workspace: Workspace,
    ) -> Generator[LicenseType, None, None]:
        """
        For the provided workspace returns which licenses are active.
        """

        return
        yield
