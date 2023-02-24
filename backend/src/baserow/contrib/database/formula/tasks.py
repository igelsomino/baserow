from datetime import timedelta
from typing import Any, Dict

from django.conf import settings
from django.utils import timezone

from celery import group

from baserow.config.celery import app
from baserow.core.models import Group


def get_query_filter_for_periodic_update(immediate: bool = False) -> Dict[str, Any]:
    """
    Returns the query filter that can be used to filter on the groups that need
    to be updated periodically.

    :param immediate: If set to true then the groups that need to be updated
    :return: The query filter that can be used to filter on the groups that need
        to be updated periodically.
    """

    query_filters = {"last_formula_periodic_update_at__isnull": False}
    if not immediate:
        query_filters[
            "last_formula_periodic_update_at__lt"
        ] = timezone.now() - timedelta(
            seconds=settings.FORMULA_NOW_MIN_TIME_BETWEEN_UPDATES_SECONDS
        )
    return query_filters


@app.task(bind=True, queue="export")
def refresh_formulas_need_periodic_update(self, immediate: bool = False):
    """
    Refreshes the formulas that need to be updated periodically for all groups.

    :param immediate: If set to true then all the groups will be refreshed
    """

    query_filters = get_query_filter_for_periodic_update(immediate)
    groups = Group.objects.filter(**query_filters)
    group_ids = [group.id for group in groups]
    group_tasks = [
        refresh_formulas_need_periodic_update_for_group.s(group_id)
        for group_id in group_ids
    ]
    group(group_tasks).apply_async()


@app.task(bind=True, queue="export")
def refresh_formulas_need_periodic_update_for_group(
    self, group_id: int, immediate: bool = False
):
    """
    Refreshes the formulas that need to be updated periodically for the provided
    group.

    :param group_id: The id of the group for which the formulas must be refreshed.
    :param immediate: If set to true then the group will be refreshed
    """

    from baserow.contrib.database.formula.handler import FormulaHandler

    query_filters = {"id": group_id, **get_query_filter_for_periodic_update(immediate)}
    try:
        group = Group.objects.get(**query_filters)
    except Group.DoesNotExist:
        return
    FormulaHandler.refresh_formulas_need_periodic_update_for_group(group)


# noinspection PyUnusedLocal
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(minutes=settings.FORMULA_NOW_PERIODIC_TASK_INTERVAL_MINUTES),
        refresh_formulas_need_periodic_update.s(),
    )
