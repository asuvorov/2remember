"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


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
