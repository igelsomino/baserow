from baserow.contrib.builder.models import Builder


class BuilderHandler:
    def get_builder(self, builder_id: int):
        return Builder.objects.get(id=builder_id)
