from typing import cast

from baserow.contrib.builder.models import Builder
from baserow.core.handler import CoreHandler


class BuilderHandler:
    def get_builder(self, builder_id: int) -> Builder:
        """
        Gets builder instance from database using its ID

        :param builder_id: ID of the builder instance you want to get
        :return: The builder model instance
        """

        return cast(
            Builder,
            CoreHandler().get_application(builder_id),
        ).specific
