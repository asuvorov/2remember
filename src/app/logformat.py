"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import json
import os
import sys
import traceback

from inspect import istraceback

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

import json_log_formatter

from decouple import config
from termcolor import cprint

# from ddcore.Serializers import JSONEncoder

from . import logconst


class JSONEncoder(DjangoJSONEncoder):
    """A custom Encoder extending the DjangoJSONEncoder."""

    def default(self, o):
        """Docstring."""
        if istraceback(o):
            return "".join(traceback.format_tb(o)).strip()

        if isinstance(o, (Exception, type)):
            return str(o)

        try:
            return super(DjangoJSONEncoder, self).default(o)
        except TypeError:
            try:
                return str(o)
            except Exception:
                return None


encoder = JSONEncoder(
    indent=4,
    sort_keys=True)


class VerboseJSONFormatter(json_log_formatter.VerboseJSONFormatter):
    """Docstring."""

    def json_record(self, message, extra, record):
        """Docstring."""
        extra.update({
            "unixtime":     int(record.created),
        })
        return super().json_record(message, extra, record)


class Format:
    """Helper Class for formatting Logs of specific Types."""

    @classmethod
    def exception(cls, exc, request_id=None, log_extra=None, **kwargs):
        """Format Exceptions with a Traceback Information.

        Parameters
        ----------
        exc                 :obj        Exception Object.
        request_id          :int        Request ID.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        _, _, exc_tb = sys.exc_info()

        log_extra.update({
            logconst.LOG_KEY_EXC_TYPE:      type(exc).__name__,
            logconst.LOG_KEY_EXC_MSG:       str(exc),
            logconst.LOG_KEY_EXC_TRACEBACK: exc_tb,
        })

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_EXCEPTION,
            log_extra=log_extra,
            file=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1],
            line=exc_tb.tb_lineno,
            request_id=request_id,
            **kwargs)

    @classmethod
    def api_detailed_info(
            cls, log_type=None, request_id=None, log_extra=None, **kwargs):
        """Format API Logs with additional Details.

        Parameters
        ----------
        log_type            :str        Log Type.
        request_id          :int        Request ID.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=log_type or logconst.LOG_VAL_TYPE_API_REQUEST,
            log_extra=log_extra,
            request_id=request_id,
            **kwargs)

    @classmethod
    def daemon_detailed_info(cls, daemon_name, operation, log_extra=None, **kwargs):
        """Format Daemon Logs with additional Details.

        Parameters
        ----------
        daemon_name         :str
        operation           :str
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_DAEMON_REQUEST,
            log_extra=log_extra,
            service=daemon_name,
            operation=operation,
            exception_message=kwargs.pop("exception_message", None),
            error=kwargs.pop("error", None),
            request_id=kwargs.pop("request_id", ""),
            status=kwargs.pop("status", logconst.LOG_VAL_STATUS_SUCCESS),
            **kwargs)

    @classmethod
    def db_error(cls, message, e0, e1, log_extra=None, **kwargs):
        """Format Database Error Logs with additional Details.

        Parameters
        ----------
        message             :str
        e0                  :obj        Error Information.
        e1                  :obj        Error Information.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_DB_ERROR,
            log_extra=log_extra,
            message=message,
            error_0=e0,
            error_1=e1)

    @classmethod
    def outage(cls, component, message="", log_extra=None, **kwargs):
        """Format Outage Logs with additional Details.

        Parameters
        ----------
        component           :obj        Service Component.
        message             :obj        Message.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_OUTAGE,
            log_extra=log_extra,
            component=component,
            message=message)

    @classmethod
    def log_detailed_info(cls, log_type, log_extra=None, **kwargs):
        """Append Type Attribute to the Log Record.

        Parameters
        ----------
        log_type            :str        Log Type.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        log_extra.update({
            logconst.LOG_KEY_ABS:                   log_type,
            logconst.LOG_KEY_ABS_ENV:               settings.ENVIRONMENT,
            logconst.LOG_KEY_NEW_RELIC_APP_NAME:    config("NEW_RELIC_APP_NAME", default="Unknown"),
            **kwargs,
        })
        return json.loads(
            json.dumps(
                dict(sorted(log_extra.items(), key=lambda item: item[0])),
                cls=JSONEncoder))
