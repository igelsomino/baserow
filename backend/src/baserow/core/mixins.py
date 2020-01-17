from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property


class OrderableMixin:
    """
    This mixin introduces a set of helpers of the model is orderable by a field.
    """

    @classmethod
    def get_highest_order_of_queryset(cls, queryset, field='order'):
        """

        :param queryset:
        :param field:
        :return:
        """

        return queryset.aggregate(
            models.Max(field)
        ).get(f'{field}__max', 0) or 0


class PolymorphicContentTypeMixin:
    """
    This mixin introduces a set of helpers for a model that has a polymorphic
    relationship with django's content type. Note that a foreignkey to the ContentType
    model must exist.

    Example:
        content_type = models.ForeignKey(
            ContentType,
            verbose_name='content type',
            related_name='applications',
            on_delete=models.SET(get_default_application_content_type)
        )
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self.__class__, 'content_type'):
            raise AttributeError(f'The attribute content_type doesn\'t exist on '
                                 f'{self.__class__.__name__}, but is required for the '
                                 f'PolymorphicContentTypeMixin.')

        if not self.id:
            if not self.content_type_id:
                self.content_type = ContentType.objects.get_for_model(self)

    @cached_property
    def specific(self):
        """Returns this instance in its most specific subclassed form."""

        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = self.specific_class
        if model_class is None:
            return self
        elif isinstance(self, model_class):
            return self
        else:
            return content_type.get_object_for_this_type(id=self.id)

    @cached_property
    def specific_class(self):
        """
        Return the class that this application would be if instantiated in its
        most specific form.
        """

        content_type = ContentType.objects.get_for_id(self.content_type_id)
        return content_type.model_class()

    def change_polymorphic_type_to(self, new_model_class):
        """
        If you for example have two polymorphic types TypeA and TypeB which both have
        unique fields, an instance with TypeA can be changed to TypeB while keeping the
        parent values and id. This method actually changes the class and sets the
        default values in the __dict__.

        :param new_model_class: The new model class that the instance must be converted
                                to.
        :type new_model_class: Model
        """

        old_fields = set([f.name for f in self._meta.get_fields()])
        new_fields = set([f.name for f in new_model_class._meta.get_fields()])
        field_names_to_remove = old_fields - new_fields
        field_names_to_add = new_fields - old_fields

        self.delete(keep_parents=True)
        self.__class__ = new_model_class
        self.content_type = ContentType.objects.get_for_model(new_model_class)

        for name in field_names_to_remove:
            del self.__dict__[name]

        for name in field_names_to_add:
            self.__dict__[name] = new_model_class._meta.get_field(name).default
