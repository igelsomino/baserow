from baserow.core.telemetry.telemetry import setup_open_telemetry_instrumentation


def post_fork(server, worker):
    setup_open_telemetry_instrumentation(add_django_instrumentation=True)
