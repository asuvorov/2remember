"""Define Models."""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


# -----------------------------------------------------------------------------
# --- Event Category Choices.
# -----------------------------------------------------------------------------
EventCategory = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_choices = [
    (EventCategory.ANIMALS,        _("Animals")),
    (EventCategory.ARTS,           _("Arts & Culture")),
    (EventCategory.YOUTH,          _("Children & Youth")),
    (EventCategory.COMMUNITY,      _("Community")),
    (EventCategory.EDUCATION,      _("Education & Literacy")),
    (EventCategory.ENVIRONMENT,    _("Environment")),
    (EventCategory.HEALTH,         _("Health & Wellness")),
    (EventCategory.RECREATION,     _("Sports & Recreation")),
    (EventCategory.SENIOURS,       _("Veterans & Seniors")),
]

EventColors = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_colors = [
    (EventColors.ANIMALS,      "DarkKhaki"),
    (EventColors.ARTS,         "LightSteelBlue"),
    (EventColors.YOUTH,        "SlateBlue"),
    (EventColors.COMMUNITY,    "DarkOrange"),
    (EventColors.EDUCATION,    "#DEB887"),
    (EventColors.ENVIRONMENT,  "Green"),
    (EventColors.HEALTH,       "Red"),
    (EventColors.RECREATION,   "LightSeaGreen"),
    (EventColors.SENIOURS,     "SaddleBrown"),
]

EventIcons = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_icons = [
    (EventIcons.ANIMALS,       "fa fa-paw fa-fw"),
    (EventIcons.ARTS,          "fa fa-wrench fa-fw"),
    (EventIcons.YOUTH,         "fa fa-child fa-fw"),
    (EventIcons.COMMUNITY,     "fa fa-users fa-fw"),
    (EventIcons.EDUCATION,     "fa fa-book fa-fw"),
    (EventIcons.ENVIRONMENT,   "fa fa-tree fa-fw"),
    (EventIcons.HEALTH,        "fa fa-heartbeat fa-fw"),
    (EventIcons.RECREATION,    "fa fa-bicycle fa-fw"),
    (EventIcons.SENIOURS,      "fa fa-home fa-fw"),
]


EventImages = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_images = [
    (EventImages.ANIMALS,       "/img/event-categories/1-animals.jpeg"),
    (EventImages.ARTS,          "/img/event-categories/2-arts-and-culture.jpeg"),
    (EventImages.YOUTH,         "/img/event-categories/3-children-and-youth.jpeg"),
    (EventImages.COMMUNITY,     "/img/event-categories/4-community.jpeg"),
    (EventImages.EDUCATION,     "/img/event-categories/5-education-and-literacy.jpeg"),
    (EventImages.ENVIRONMENT,   "/img/event-categories/6-environment-2.jpeg"),
    (EventImages.HEALTH,        "/img/event-categories/7-health-and-wellness.jpeg"),
    (EventImages.RECREATION,    "/img/event-categories/8-sports-and-recreation.jpeg"),
    (EventImages.SENIOURS,      "/img/event-categories/9-veterans-and-seniors.jpeg"),
]


# -----------------------------------------------------------------------------
# --- Event Choices.
# -----------------------------------------------------------------------------
EventStatus = enum(
    DRAFT="0",
    UPCOMING="1",
    COMPLETE="2",
    EXPIRED="4",
    CLOSED="8")
event_status_choices = [
    (EventStatus.DRAFT,    _("Draft")),
    (EventStatus.UPCOMING, _("Upcoming")),
    (EventStatus.COMPLETE, _("Complete")),
    (EventStatus.EXPIRED,  _("Expired")),
    (EventStatus.CLOSED,   _("Closed")),
]

EventMode = enum(
    FREE_FOR_ALL="0",
    CONFIRMATION_REQUIRED="1")
application_choices = [
    (EventMode.FREE_FOR_ALL,            _("Anyone can participate.")),
    (EventMode.CONFIRMATION_REQUIRED,   _("Participate only after a confirmed Application")),
]


# -----------------------------------------------------------------------------
# --- Role Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Participation Choices.
# -----------------------------------------------------------------------------
ParticipationRemoveMode = enum(
    REMOVE_APPLICATION="0",
    REJECT_APPLICATION="1",
    REJECT_SELFREFLECTION="2",
    ACKNOWLEDGE="4")

ParticipationStatus = enum(
    WAITING_FOR_CONFIRMATION="0",
    CONFIRMATION_DENIED="1",
    CONFIRMED="2",
    CANCELLED_BY_ADMIN="4",
    CANCELLED_BY_USER="8",
    WAITING_FOR_SELFREFLECTION="16",
    WAITING_FOR_ACKNOWLEDGEMENT="32",
    ACKNOWLEDGED="64")
participation_status_choices = [
    (ParticipationStatus.WAITING_FOR_CONFIRMATION,
        _("Waiting for Confirmation")),
    (ParticipationStatus.CONFIRMATION_DENIED,
        _("You were not accepted to this Event")),
    (ParticipationStatus.CONFIRMED,
        _("Signed up")),
    (ParticipationStatus.CANCELLED_BY_ADMIN,
        _("The Organizer removed you from this Event")),
    (ParticipationStatus.CANCELLED_BY_USER,
        _("You withdrew your Participation to this Event")),
    (ParticipationStatus.WAITING_FOR_SELFREFLECTION,
        _("Please, write your Experience Report")),
    (ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
        _("Waiting for Acknowledgment")),
    (ParticipationStatus.ACKNOWLEDGED,
        _("Report acknowledged")),
]


# -----------------------------------------------------------------------------
# --- Recurrence Choices.
# -----------------------------------------------------------------------------
Recurrence = enum(
    DATELESS="0",
    ONCE="1")
recurrence_choices = [
    (Recurrence.DATELESS,   _("Dateless")),
    (Recurrence.ONCE,       _("Once")),
]

Month = enum(
    NONE="",
    JANUARY="1",
    FEBRUARY="2",
    MARCH="3",
    APRIL="4",
    MAY="5",
    JUNE="6",
    JULY="7",
    AUGUST="8",
    SEPTEMBER="9",
    OCTOBER="10",
    NOVEMBER="11",
    DECEMBER="12")
month_choices = [
    (Month.NONE,        _("----------")),
    (Month.JANUARY,     _("January")),
    (Month.FEBRUARY,    _("February")),
    (Month.MARCH,       _("March")),
    (Month.APRIL,       _("April")),
    (Month.MAY,         _("May")),
    (Month.JUNE,        _("June")),
    (Month.JULY,        _("July")),
    (Month.AUGUST,      _("August")),
    (Month.SEPTEMBER,   _("September")),
    (Month.OCTOBER,     _("October")),
    (Month.NOVEMBER,    _("November")),
    (Month.DECEMBER,    _("December")),
]

DayOfWeek = enum(
    NONE="",
    SUNDAY="0",
    MONDAY="1",
    TUESDAY="2",
    WEDNESDAY="3",
    THURSDAY="4",
    FRIDAY="5",
    SATURDAY="6")
day_of_week_choices = [
    (DayOfWeek.NONE,        _("----------")),
    (DayOfWeek.SUNDAY,      _("Sunday")),
    (DayOfWeek.MONDAY,      _("Monday")),
    (DayOfWeek.TUESDAY,     _("Tuesday")),
    (DayOfWeek.WEDNESDAY,   _("Wednesday")),
    (DayOfWeek.THURSDAY,    _("Thursday")),
    (DayOfWeek.FRIDAY,      _("Friday")),
    (DayOfWeek.SATURDAY,    _("Saturday")),
]

day_of_month_choices = [(str(day), str(day)) for day in range(0, 32)]
day_of_month_choices[0] = ("", _("----------"))
day_of_month_choices.append(("32", _("Last Day of Month")))
