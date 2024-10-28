"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from .models import (
    EventCategory, event_category_choices,
    EventCategoryColors, event_category_colors,
    EventCategoryIcons, event_category_icons,
    EventCategoryImages, event_category_images,
    # EventMode,
    # EventStatus,
    # ParticipationRemoveMode,
    # ParticipationStatus, participation_status_choices,
    # Month, month_choices,
    # DayOfWeek, day_of_week_choices,
    # day_of_month_choices
    )


def pb_event_choices(request):
    """Docstring."""
    return {
        "EventCategory":            EventCategory,
        "event_category_choices":   event_category_choices,
        "EventCategoryColors":      EventCategoryColors,
        "event_category_colors":    event_category_colors,
        "EventCategoryIcons":       EventCategoryIcons,
        "event_category_icons":     event_category_icons,
        "EventCategoryImages":      EventCategoryImages,
        "event_category_images":    event_category_images,
        # "EventStatus":              EventStatus,
        # "EventMode":                EventMode,
    }


def pb_participation_choices(request):
    """Docstring."""
    return {
        # "ParticipationRemoveMode":      ParticipationRemoveMode,
        # "ParticipationStatus":          ParticipationStatus,
        # "participation_status_choices": participation_status_choices,
    }
