import logging
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import ProxyTracerProvider

logger = logging.getLogger(__name__)


def setup_open_telemetry_instrumentation(add_django_instrumentation: bool):
    """
    When the env var BASEROW_ENABLE_OTEL is set to any non-blank string and this
    function is called metrics will be setup and sent according to the OTEL env vars
    you can find described at:
    - https://opentelemetry.io/docs/reference/specification/protocol/exporter/
    - https://opentelemetry.io/docs/reference/specification/sdk-environment-variables/

    :param add_django_instrumentation: Enables specific instrumentation for a django
        process that is processing requests. Don't enable this for a celery process etc.
    """

    if bool(os.getenv("BASEROW_ENABLE_OTEL", False)):
        existing_provider = trace.get_tracer_provider()
        if not isinstance(existing_provider, ProxyTracerProvider):
            print("Provider already configured not reconfiguring...")
        else:
            provider = TracerProvider()
            processor = BatchSpanProcessor(OTLPSpanExporter())
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)

            _setup_standard_backend_instrumentation()

            print("Configured default backend instrumentation")
            if add_django_instrumentation:
                print("Adding Django request instrumentation also.")
                _setup_django_process_instrumentation()

            print("Telemetry enabled!")
    else:
        print("Not configuring telemetry due to BASEROW_ENABLE_OTEL not being set.")


def _setup_standard_backend_instrumentation():
    BotocoreInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()
    RedisInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    CeleryInstrumentor().instrument()


def _setup_django_process_instrumentation():
    def response_hook(span, request, response):
        if hasattr(request, "user"):
            span.set_attribute("user.id", request.user.id)
            if hasattr(request.user, "email"):
                span.set_attribute("user.email", request.user.email)
            if hasattr(request.user, "first_name"):
                span.set_attribute("user.first_name", request.user.first_name)
            if hasattr(request.user, "untrusted_client_session_id"):
                span.set_attribute(
                    "user.untrusted_client_session_id",
                    request.user.untrusted_client_session_id,
                )
        if hasattr(request, "user_token"):
            span.set_attribute("user.token_id", request.user_token.id)

    DjangoInstrumentor().instrument(
        response_hook=response_hook,
    )
