from baserow.contrib.builder.operations import BuilderOperationType


class CreatePageOperationType(BuilderOperationType):
    type = "builder.page.create"


class DeletePageOperationType(BuilderOperationType):
    type = "builder.page.delete"
