from typing import cast

from baserow.contrib.builder.models import Builder
from baserow.core.handler import CoreHandler


class BuilderHandler:
    def get_builder(self, builder_id: int) -> Builder:
        return cast(
            Builder,
            CoreHandler().get_application(builder_id),
        ).specific
