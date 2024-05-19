"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

# from apscheduler.schedulers.background import BackgroundScheduler
# from haystack.management.commands import rebuild_index


# background_scheduler = BackgroundScheduler()


# # -----------------------------------------------------------------------------
# # --- Start all the scheduled Tasks
# # -----------------------------------------------------------------------------
# def start_all():
#     """Start all of the Cron Tasks."""
#     background_scheduler.start()


# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~
# # ~~~ TASKS
# # ~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # -----------------------------------------------------------------------------
# # --- System Ping
# # -----------------------------------------------------------------------------
# # @background_scheduler.scheduled_job("interval", minutes=1)
# def system_ping():
#     """Docstring."""
#     # now = datetime.datetime.now()


# # -----------------------------------------------------------------------------
# # --- Rebuild Search Indexes.
# #     A periodic Task that runs every 3 Hours at 0 Minutes.
# # -----------------------------------------------------------------------------
# @background_scheduler.scheduled_job("interval", hours=3)
# def rebuild_search_indexes():
#     """Rebuild/update Search Indexes.

#     https://stackoverflow.com/questions/4358771/updating-a-haystack-search-index-with-django-celery
#     """
#     try:
#         rebuild_index.Command().handle(
#             age=4,
#             batchsize=1000,
#             workers=0,
#             max_retries=5,
#             interactive=False,
#             remove=True,
#             verbosity=2,
#             using=["default", ])
#         # update_index.Command().handle(
#         #     age=4,
#         #     interactive=False,
#         #     remove=True,
#         #     verbosity=2,
#         #     using=["default", ])

#         # ---------------------------------------------------------------------
#         # --- Save the Log

#     except Exception as exc:
#         print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

#         # ---------------------------------------------------------------------
#         # --- Save the Log

#     return True


# # -----------------------------------------------------------------------------
# # --- Call the `main` Function.
# # -----------------------------------------------------------------------------
# start_all()
