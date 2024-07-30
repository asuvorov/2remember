"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import functools
import inspect
import logging
import tracemalloc

from time import perf_counter

from django.http import HttpRequest

from termcolor import cprint, colored

from . import logconst
from .logformat import Format


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def log_default(
        _func=None, *, my_logger: logging.Logger = None, cls_or_self = True):
    """Default logging Decorator.

    Parameters
    ----------
    _func                   :obj        Function Object.
    my_logger               :obj        Logger Object.
    cls_or_self             :bool       Is a Class or Instance Method?
    verbose                 :bool       Is a Verbosity?

    Returns
    -------

    Raises
    ------
    """
    def log_default_info(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # -----------------------------------------------------------------
            # --- Initials.
            # -----------------------------------------------------------------
            # --- Manage `self` or `cls`.
            _self = None
            if cls_or_self:
                _self = args[0]

            func_name = f"{_self.__class__.__name__}.{func.__name__}" if _self else func.__name__

            # -----------------------------------------------------------------
            # --- Manage Logger.
            logger = my_logger
            if my_logger is None:
                logger = logging.getLogger(func.__name__)

            log_type = logconst.LOG_VAL_TYPE_FUNC_CALL
            log_extra = {
                "func_name":                func_name,
                "func_args":                args,
                "func_kwargs":              kwargs,
                "logger":                   logger,
                logconst.LOG_KEY_STATUS:    logconst.LOG_VAL_STATUS_SUCCESS,
            }

            # -----------------------------------------------------------------
            # --- Manage Request and Response.
            request_id = None
            for a in args:
                if isinstance(a, HttpRequest):
                    log_type = logconst.LOG_VAL_TYPE_FRONT_END_REQUEST
                    request_id = a.request_id
                    break

            # -----------------------------------------------------------------
            # --- Logging.
            # -----------------------------------------------------------------
            cprint(f"***" * 27, "green")
            cprint(f"*** INSIDE  `{func_name}`", "green")

            args_repr = "\n                        ".join([repr(a) for a in args])
            kwargs_repr = "\n                        ".join([f"{k}={v!r}" for k, v in kwargs.items()])

            cprint(f"    [--- DUMP ---]   ARGS : {args_repr}", "yellow")
            cprint(f"                   KWARGS : {kwargs_repr}", "yellow")

            try:
                tracemalloc.start()
                start_time = perf_counter()
                res = func(*args, **kwargs)
                return res
            except Exception as exc:
                cprint(f"### EXCEPTION in `{func_name}`:\n",
                       f"                  {type(exc).__name__}\n"
                       f"                  {str(exc)}", "red", "on_white")

                log_extra[logconst.LOG_KEY_STATUS] = logconst.LOG_VAL_STATUS_FAILURE
                logger.exception("", extra=Format.exception(
                    exc=exc,
                    request_id=request_id,
                    log_extra=log_extra))

                raise exc
            else:
                pass
            finally:
                current, peak = tracemalloc.get_traced_memory()
                end_time = perf_counter()
                tracemalloc.stop()

                cprint(f"*** LEAVING   `{func_name}`", "green")
                cprint(f"*** MEM USE  : {current / 10**6:.6f} MB", "yellow")
                cprint(f"    MEM PEAK : {peak / 10**6:.6f} MB", "yellow")
                cprint(f"    TOOK     : {end_time - start_time:.6f} sec", "yellow")
                cprint(f"***" * 27, "green")

                log_extra.update({
                    logconst.LOG_KEY_ABS_EXEC_TIME: f"{end_time - start_time:.6f}",
                    logconst.LOG_KEY_ABS_MEM_USAGE: f"{current / 10**6:.6f}",
                    logconst.LOG_KEY_ABS_MEM_PEAK:  f"{peak / 10**6:.6f}",
                })
                logger.info("", extra=Format.api_detailed_info(
                    log_type=log_type,
                    request_id=request_id,
                    log_extra=log_extra))

        return wrapper

    if _func is None:
        return log_default_info

    return log_default_info(_func)
