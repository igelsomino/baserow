# Job system refactoring

## Goal

We want our job system to be able to:
1. limit the concurrent number of running jobs per user, letting the user add more async-jobs to the queue even if there's no workers capacity at that time
1. Make the `max_concurrent_jobs_per_user` and `max_enqueable_jobs_per_user` customizable (not sure if we want to make them customizable also for free/premium). 
1. detect if the task crash without updating its metadata in the DB (e.g. the worker restarts/die unexpectedly) and clean it automatically
1. let the user be able to abort tasks (we cannot know beforehand how long the task will take to finish, so the user might change the idea after the async-job is already started)
1. refactor and unify the backend and the frontend to use WebSockets for progress updates and share the same abstractions everywhere
1. Add an element in the UI to keep track of the long-running operations with an option to abort or restart the single job.


## Status
Current limitations are:
1. the `JobType.max_count` is per user and job_type. This limit is not for the concurrent running jobs but stops the user from adding more jobs to the queue, returning an error in the GUI if a user submits, let's say, two `duplicate_table` jobs before the first finishes.
1. The limit setting is per `JobType` instead of per user/group and is not customizable.
1. The `clean_up_jobs` automatically deletes jobs started more than `BASEROW_JOB_SOFT_TIME_LIMIT` seconds ago. The default is 30 minutes so we need to wait that time to be able to start the same job again in case the task crash unexpectedly during the execution. It also means a job cannot take longer than that without the high risk of being deleted. Task like the audit log export of million of rows can take several minutes to finish, so probably it's better to look at the time ellapsed since the last progress, maybe?
1. The first implementation of `ExportJob` is not a `JobType` even if it share many similar concepts and should be refactor as described in [#1496](https://gitlab.com/bramw/baserow/-/issues/1496). 
1. The frontend uses 3 different long-polling mechanisms to update the show the current job progress. We probably want to start using websockets for progress updates.
1. There isn't a central notification/job progress panel to look at to know which job is running and possibly stop it.

## Context

### Notes about Celery - the task queue
1. There is no simple way to limit the number of tasks workers can process per user once the tasks are added to a queue. In order to avoid the possibility for a single user to use all the resources available but still let him add a certain number of tasks to the queue, we need to add some scheduling logic before the task is submitted to the queue. 
1. It's not super-easy to check if a `task` is still running or not. The `AsyncResult` Celery class returns `"PENDING"` both for unknown `task_id` or pending or crashed tasks so it doesn't help to distinguish between the different cases. Even adding the DB as result backend and activating the `CELERY_TASK_TRACK_STARTED` option, we have no guarantee the task is actually running without checking let's say if the worker id is still alive. (Note: calling `app.control.inspect().active() from the CLI takes more than 1 second to run`)
1. To make the task `abortable` we need our tasks to extend the [AbortableTask](`https://docs.celeryq.dev/en/stable/reference/celery.contrib.abortable.html`) and every single long task should check `is_abort()` as often as possible to interrupt the current work. The other option we have is to split long tasks in multiple fast ones wherever is possible and chain or group them, so we can probably simply use [revoke](https://docs.celeryq.dev/en/stable/userguide/workers.html#revoke-revoking-tasks), but in that case we should also think how to rollback to the original state.


## Decision
1. API views stop submitting `jobs` directly to a celery queues, they just create a new job of the correct `JobType` and start a `schedule_job_to_run` celery task instead.
1. The `schedule_job_to_run` task will:
    1. look for users with `nr_concurrent_jobs_per_user` <= `max_concurrent_jobs_per_user` and run the oldest pending job.
    1. look for running jobs created more than `SOFT_TIME_LIMIT` ago and check if they're actually running. We can maybe check the last `progress_key` update in the cache or if the worker id is still alive
    1. At the end of every job, the `JobHandler.run` will start again the `schedule_job_to_run` celery task to immediately start a new job for users with pending ones. 
    1. be called periodically (1 minute?) by the celery-beat to ensure `jobs` are scheduled correctly and update/clean possible stale states.
1. Create a job progress widget in the UI to show the progress of the running jobs and the other jobs in the queue waiting to start.
1. Start using websockets to handle job updates from the backend and fallback to the polling mechanism is something goes wrong with the socket.

**NOTE**: The `schedule_job_to_run` should use locks accordingly to avoid race conditions between different istances of the same task. 


## Consequences
1. Users can enqueue multiple jobs of the same or different types up to some limit and all the operations will take eventually using up to some pre-defined amount of resources.
1. Using websockets instead of the REST API we should decrease the amount of requests and make the job progress update more responsive.
1. Users can stop long tasks once started and look in a central place in the UI for progresses
1. Introduce a concept of `task scheduling` before the task is actually submitted to celery that can come in handy also for future `workflow` automation purposes.