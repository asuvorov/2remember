"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from .models import (
    EventCategory, event_category_choices,
    EventColors, event_category_colors,
    EventIcons, event_category_icons,
    EventImages, event_category_images,
    EventMode,
    EventStatus,
    ParticipationRemoveMode,
    ParticipationStatus, participation_status_choices,
    Recurrence, recurrence_choices,
    Month, month_choices,
    DayOfWeek, day_of_week_choices,
    day_of_month_choices)


def pb_event_choices(request):
    """Docstring."""
    return {
        "EventCategory":            EventCategory,
        "event_category_choices":   event_category_choices,
        "EventColors":              EventColors,
        "event_category_colors":    event_category_colors,
        "EventIcons":               EventIcons,
        "event_category_icons":     event_category_icons,
        "EventImages":              EventImages,
        "event_category_images":    event_category_images,
        "EventStatus":              EventStatus,
        "EventMode":                EventMode,
    }


def pb_participation_choices(request):
    """Docstring."""
    return {
        "ParticipationRemoveMode":      ParticipationRemoveMode,
        "ParticipationStatus":          ParticipationStatus,
        "participation_status_choices": participation_status_choices,
    }


def pb_recurrence_choices(request):
    """Docstring."""
    return {
        "Recurrence":           Recurrence,
        "recurrence_choices":   recurrence_choices,
        "Month":                Month,
        "month_choices":        month_choices,
        "DayOfWeek":            DayOfWeek,
        "day_of_week_choices":  day_of_week_choices,
        "day_of_month_choices": day_of_month_choices,
    }
