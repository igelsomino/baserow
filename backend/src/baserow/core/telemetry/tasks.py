import os

from celery.signals import worker_process_init

from baserow.core.telemetry.telemetry import setup_open_telemetry_instrumentation


@worker_process_init.connect
def initialize_otel(**kwargs):
    print(f"opentelemetry initialization in process pid {os.getpid()}")
    setup_open_telemetry_instrumentation(add_django_instrumentation=False)
