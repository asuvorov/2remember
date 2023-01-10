"""Define Context Processors."""

from .choices import (
    EventStatus,
    EventMode,
    EventCategory, event_category_choices,
    EventColors, event_category_colors,
    EventIcons, event_category_icons,
    EventImages, event_category_images,
    ParticipationRemoveMode,
    ParticipationStatus, participation_status_choices,
    Recurrence, recurrence_choices,
    Month, month_choices,
    DayOfWeek, day_of_week_choices,
    day_of_month_choices)


def pb_event_choices(request):
    """Docstring."""
    return {
        "EventStatus":             EventStatus,
        "EventMode":               EventMode,
        "EventCategory":           EventCategory,
        "event_category_choices":   event_category_choices,
        "EventColors":             EventColors,
        "event_category_colors":    event_category_colors,
        "EventIcons":              EventIcons,
        "event_category_icons":     event_category_icons,
        "EventImages":             EventImages,
        "event_category_images":    event_category_images,
    }


def pb_participation_choices(request):
    """Docstring."""
    return {
        "ParticipationStatus":         ParticipationStatus,
        "ParticipationRemoveMode":    ParticipationRemoveMode,
        "participation_status_choices": participation_status_choices,
    }


def pb_recurrence_choices(request):
    """Docstring."""
    return {
        "Recurrence":                   Recurrence,
        "recurrence_choices":           recurrence_choices,
        "Month":                        Month,
        "month_choices":                month_choices,
        "DayOfWeek":                  DayOfWeek,
        "day_of_week_choices":          day_of_week_choices,
        "day_of_month_choices":         day_of_month_choices,
    }
