"""Define Tasks."""

import datetime

from django.conf import settings
from django.utils.translation import gettext as _

from apscheduler.schedulers.background import BackgroundScheduler

from ddcore.SendgridUtil import send_templated_email

from .models import Event


background_scheduler = BackgroundScheduler()


# -----------------------------------------------------------------------------
# --- Start all the scheduled Tasks
# -----------------------------------------------------------------------------
def start_all():
    """Start all of the Cron Tasks."""
    background_scheduler.start()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ TASKS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -----------------------------------------------------------------------------
# --- Notify Admins about overdue Events.
#     A periodic Task that runs every Midnight.
# -----------------------------------------------------------------------------
@background_scheduler.scheduled_job("cron", hour="0", minute="0", day_of_week="*")
def event_overdue_notify_admin():
    """Docstring."""
    try:
        upcoming_events = Event.objects.get_upcoming()

        for event in upcoming_events:
            if event.is_overdue:
                # -------------------------------------------------------------
                # --- Render HTML Email Content
                greetings = _(
                    "Dear, %(user)s.") % {
                        "user":     event.author.first_name,
                    }
                htmlbody = _(
                    "<p>Your Event \"<a href=\"%(url)s\">%(name)s</a>\" is overdue!</p>"
                    "<p>If this Event has taken place as planned, please, mark it as completed.</p>"
                    "<p>Remember to remove all Participants from the Event, who did not show up to help, so the Event will not appear on their Profiles.</p>") % {
                        "url":      event.public_url(),
                        "name":     event.name,
                    }

                # -------------------------------------------------------------
                # --- Send Notification to Event Admin
                send_templated_email(
                    template_subj={
                        "name":     "events/emails/event_overdue_subject.txt",
                        "context":  {},
                    },
                    template_text={
                        "name":     "events/emails/event_overdue.txt",
                        "context": {
                            "admin":            event.author,
                            "event":        event,
                            "event_link":   event.public_url(),
                        },
                    },
                    template_html={
                        "name":     "emails/base.html",
                        "context": {
                            "greetings":    greetings,
                            "htmlbody":     htmlbody,
                        },
                    },
                    from_email=settings.EMAIL_SENDER,
                    to=[
                        event.author.email,
                    ],
                    headers=None,
                )

        # ---------------------------------------------------------------------
        # --- Save the Log

    except Exception as exc:
        # ---------------------------------------------------------------------
        # --- Save the Log
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    return True


# -----------------------------------------------------------------------------
# --- Notify Event Participants about upcoming Events.
#     A periodic Task that runs every 1am.
# -----------------------------------------------------------------------------
@background_scheduler.scheduled_job("cron", hour="0", minute="0", day_of_week="*")
def event_upcoming_notify():
    """Docstring."""
    try:
        upcoming_events = Event.objects.get_upcoming()

        for event in upcoming_events:
            days_delta = (event.start_date - datetime.date.today()).days

            if 0 < days_delta <= 2:
                for participation in event.event_participations.confirmed():
                    # ---------------------------------------------------------
                    # --- Render HTML Email Content
                    greetings = _(
                        "Dear, %(user)s.") % {
                            "user":     participation.user.first_name,
                        }
                    htmlbody = _(
                        "<p>Don\'t forget that you are signed up for the Event \"<a href=\"%(url)s\">%(name)s</a>\" on %(start_date)s at %(start_time)s.</p>"
                        "<p>Please, don\'t forget to show up!</p>") % {
                            "url":          event.public_url(),
                            "name":         event.name,
                            "start_date":   event.get_start_date,
                            "start_time":   event.get_start_time,
                        }

                    # ---------------------------------------------------------
                    # --- Send Notification to the Event Participants
                    send_templated_email(
                        template_subj={
                            "name":     "events/emails/event_upcoming_subject.txt",
                            "context":  {},
                        },
                        template_text={
                            "name":     "events/emails/event_upcoming.txt",
                            "context": {
                                "user":             participation.user,
                                "event":        event,
                                "event_link":   event.public_url(),
                            },
                        },
                        template_html={
                            "name":     "emails/base.html",
                            "context": {
                                "greetings":    greetings,
                                "htmlbody":     htmlbody,
                            },
                        },
                        from_email=settings.EMAIL_SENDER,
                        to=[
                            participation.user.email,
                        ],
                        headers=None,
                    )

        # ---------------------------------------------------------------------
        # --- Save the Log

    except Exception as exc:
        # ---------------------------------------------------------------------
        # --- Save the Log
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    return True


# -----------------------------------------------------------------------------
# --- Call the `main` Function.
# -----------------------------------------------------------------------------
start_all()
