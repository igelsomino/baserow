from contextlib import contextmanager
from typing import Callable, Dict, Optional, Tuple, Type, Union

from django.utils.encoding import force_str

from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from baserow.core.exceptions import InstanceTypeDoesNotExist

from .exceptions import RequestBodyValidationException

ErrorTupleType = Tuple[str, int, str]
ExceptionMappingType = Dict[
    Type[Exception],
    Union[
        str,
        ErrorTupleType,
        Callable[
            [
                Exception,
            ],
            Optional[Union[str, ErrorTupleType]],
        ],
    ],
]


@contextmanager
def map_exceptions(mapping: ExceptionMappingType):
    """
    This utility function simplifies mapping uncaught exceptions to a standard api
    response exception.

    Example:
      with map_api_exceptions({ SomeException: 'ERROR_1' }):
          raise SomeException('This is a test')

      HTTP/1.1 400
      {
        "error": "ERROR_1",
        "detail": "This is a test"
      }

    Example 2:
      with map_api_exceptions({ SomeException: ('ERROR_1', 404, 'Other message') }):
          raise SomeException('This is a test')

      HTTP/1.1 404
      {
        "error": "ERROR_1",
        "detail": "Other message"
      }

    Example 3:
      with map_api_exceptions(
          {
              SomeException: lambda e: ('ERROR_1', 404, 'Conditional Error')
              if "something" in str(e)
              else None
          }
      ):
          raise SomeException('something')

      HTTP/1.1 404
      {
        "error": "ERROR_1",
        "detail": "Conditional Error"
      }

    Example 4:
      with map_api_exceptions(
          {
              SomeException: lambda e: ('ERROR_1', 404, 'Conditional Error')
              if "something" in str(e)
              else None
          }
      ):
          raise SomeException('doesnt match')

      # SomeException will be thrown directly if the provided callable returns None.
    """

    from baserow.api.registries import api_exception_registry

    registered_exceptions = api_exception_registry.get_all()
    for ex in registered_exceptions:
        mapping[ex.exception_class] = ex.exception_error

    try:
        yield
    except tuple(mapping.keys()) as e:
        value = _search_up_class_hierarchy_for_mapping(e, mapping)
        status_code = status.HTTP_400_BAD_REQUEST
        detail = ""

        if callable(value):
            value = value(e)
            if value is None:
                raise e
        if isinstance(value, str):
            error = value
        if isinstance(value, tuple):
            error = value[0]
            if len(value) > 1 and value[1] is not None:
                status_code = value[1]
            if len(value) > 2 and value[2] is not None:
                detail = value[2].format(e=e)

        exc = APIException({"error": error, "detail": detail})
        exc.status_code = status_code

        raise exc


def _search_up_class_hierarchy_for_mapping(e, mapping):
    for clazz in e.__class__.mro():
        value = mapping.get(clazz)
        if value:
            return value
    return None


def validate_data(
    serializer_class,
    data,
    partial=False,
    exception_to_raise=RequestBodyValidationException,
    many=False,
    return_validated=False,
    context=None,
):
    """
    Validates the provided data via the provided serializer class. If the data doesn't
    match with the schema of the serializer an api exception containing more detailed
    information will be raised.

    :param serializer_class: The serializer that must be used for validating.
    :type serializer_class: Serializer
    :param data: The data that needs to be validated.
    :type data: dict
    :param partial: Whether the data is a partial update.
    :type partial: bool
    :param many: Indicates whether the serializer should be constructed as a list.
    :type many: bool
    :param return_validated: Returns validated_data from DRF serializer
    :type return_validated: bool
    :param context: The context that is passed to the serializer.
    :type context: dict or None
    :return: The data after being validated by the serializer.
    :rtype: dict
    """

    def serialize_errors_recursive(error):
        if isinstance(error, dict):
            return {
                key: serialize_errors_recursive(errors) for key, errors in error.items()
            }
        elif isinstance(error, list):
            return [serialize_errors_recursive(errors) for errors in error]
        else:
            return {"error": force_str(error), "code": error.code}

    serializer = serializer_class(
        data=data, partial=partial, many=many, context=context
    )
    if not serializer.is_valid():
        detail = serialize_errors_recursive(serializer.errors)
        raise exception_to_raise(detail)

    if return_validated:
        return serializer.validated_data

    return serializer.data


def validate_data_custom_fields(
    type_name,
    registry,
    data,
    base_serializer_class=None,
    type_attribute_name="type",
    partial=False,
    allow_empty_type=False,
    context=None,
):
    """
    Validates the provided data with the serializer generated by the registry based on
    the provided type_name and provided base_serializer_class.

    :param type_name: The type name of the type instance that is needed to generated
        the serializer.
    :type type_name: str
    :param registry: The registry where to get the type instance from.
    :type registry: Registry
    :param data: The data that needs to be validated.
    :type data: dict
    :param base_serializer_class: The base serializer class that is used when
        generating the serializer for validation.
    :type base_serializer_class: ModelSerializer
    :param type_attribute_name: The attribute key name that contains the type value.
    :type type_attribute_name: str
    :param partial: Whether the data is a partial update.
    :type partial: bool
    :param allow_empty_type: Whether the type can be empty.
    :type allow_empty_type: bool
    :param context: The context that is passed to the serializer.
    :type context: dict or None
    :raises RequestBodyValidationException: When the type is not a valid choice.
    :return: The validated data.
    :rtype: dict
    """

    if not type_name and allow_empty_type:
        serializer_class = base_serializer_class
    else:
        try:
            type_instance = registry.get(type_name)
        except InstanceTypeDoesNotExist:
            # If the provided type name doesn't exist we will raise a machine
            # readable validation error.
            raise RequestBodyValidationException(
                {
                    type_attribute_name: [
                        {
                            "error": f'"{type_name}" is not a valid choice.',
                            "code": "invalid_choice",
                        }
                    ]
                }
            )
        else:
            serializer_kwargs = {
                "base_class": base_serializer_class,
                # We want the request serializer as we are validating date from a
                # request
                "request_serializer": True,
            }
            serializer_class = type_instance.get_serializer_class(**serializer_kwargs)

    return validate_data(serializer_class, data, partial=partial, context=context)


def get_request(args):
    """
    A small helper function that checks if the request is in the args and returns that
    request.

    :param args: A list containing the original arguments of the called view method.
    :type args: list
    :raises ValueError: When the request has not been found in the args.
    :return: The extracted request object.
    :rtype: Request
    """

    if len(args) < 2 or not isinstance(args[1], Request):
        raise ValueError("There must be a request in the args.")

    return args[1]


def type_from_data_or_registry(
    data, registry, model_instance, type_attribute_name="type"
):
    """
    Returns the type in the provided data else the type will be returned via the
    registry.

    :param data: The data that might contains the type name.
    :type data: dict
    :param registry: The registry where to get the type instance from if not provided in
        the data.
    :type registry: Registry
    :param model_instance: The model instance we want to know the type from if not
        provided in the data.
    :type model_instance: Model
    :param type_attribute_name: The expected type attribute name in the data.
    :type type_attribute_name: str
    :return: The extracted type.
    :rtype: str
    """

    if type_attribute_name in data:
        return data[type_attribute_name]
    else:
        return registry.get_by_model(model_instance.specific_class).type


def get_serializer_class(
    model,
    field_names,
    field_overrides=None,
    base_class=None,
    meta_ref_name=None,
    required_fields=None,
    base_mixins=None,
    meta_extra_kwargs=None,
):
    """
    Generates a model serializer based on the provided field names and field overrides.

    :param model: The model class that must be used for the ModelSerializer.
    :type model: Model
    :param field_names: The model field names that must be added to the serializer.
    :type field_names: list
    :param field_overrides: A dict containing field overrides where the key is the name
        and the value must be a serializer Field.
    :type field_overrides: dict
    :param base_class: The class that must be extended.
    :type base_class: ModelSerializer
    :param meta_ref_name: Optionally a custom ref name can be set. If not provided,
        then the class name of the model and base class are used.
    :type meta_ref_name: str
    :param required_fields: List of field names that should be present even when
        performing partial validation.
    :type required_fields: list[str]
    :param mixins: An optional list of mixins that must be added to the serializer.
    :type base_mixins: list[serializers.Serializer]
    :param meta_extra_kwargs: An optional dict containing extra kwargs for the Meta
        class.
    :type meta_extra_kwargs: dict or None
    :return: The generated model serializer containing the provided fields.
    :rtype: ModelSerializer
    """

    model_ = model

    if not field_overrides:
        field_overrides = {}

    if not meta_ref_name:
        meta_ref_name = model_.__name__

        if base_class:
            meta_ref_name += base_class.__name__

    if not base_class:
        base_class = ModelSerializer

    extends_meta = object
    meta_extra_kwargs = meta_extra_kwargs or {}

    if hasattr(base_class, "Meta"):
        extends_meta = getattr(base_class, "Meta")
        field_names = list(extends_meta.fields) + list(field_names)
        meta_extra_kwargs.update(getattr(extends_meta, "extra_kwargs", {}))

    class Meta(extends_meta):
        ref_name = meta_ref_name
        model = model_
        fields = list(field_names)
        extra_kwargs = meta_extra_kwargs

    attrs = {"Meta": Meta}

    if field_overrides:
        attrs.update(field_overrides)

    def validate(self, value):
        if required_fields:
            for field_name in required_fields:
                if field_name not in value:
                    raise serializers.ValidationError(
                        {f"{field_name}": "This field is required."}
                    )

        return value

    attrs["validate"] = validate
    mixins = base_mixins or []
    return type(
        str(model_.__name__ + "Serializer"),
        (
            *mixins,
            base_class,
        ),
        attrs,
    )


class MappingSerializer:
    """
    A placeholder class for the `MappingSerializerExtension` extension class.
    """

    def __init__(self, component_name, mapping, name, many=False):
        self.read_only = False
        self.component_name = component_name
        self.mapping = mapping
        self.name = name
        self.many = many
        self.partial = False


class CustomFieldRegistryMappingSerializer:
    """
    A placeholder class for the `CustomFieldRegistryMappingSerializerExtension`
    extension class.
    """

    def __init__(self, registry, base_class, many=False):
        self.read_only = False
        self.registry = registry
        self.base_class = base_class
        self.many = many
        self.partial = False


class DiscriminatorCustomFieldsMappingSerializer:
    """
    A placeholder class for the `DiscriminatorCustomFieldsMappingSerializerExtension`
    extension class.
    """

    def __init__(
        self,
        registry,
        base_class,
        type_field_name="type",
        many=False,
        help_text=None,
        request=False,
    ):
        self.read_only = False
        self.registry = registry
        self.base_class = base_class
        self.type_field_name = type_field_name
        self.many = many
        self.help_text = help_text
        self.partial = False
        self.request = request


class DiscriminatorMappingSerializer:
    """
    A placeholder class for the `DiscriminatorMappingSerializerExtension` extension
    class.
    """

    def __init__(self, component_name, mapping, type_field_name="type", many=False):
        self.read_only = False
        self.component_name = component_name
        self.mapping = mapping
        self.type_field_name = type_field_name
        self.many = many
        self.partial = False
