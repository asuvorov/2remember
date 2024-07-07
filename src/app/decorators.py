"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import functools
import inspect
import logging
import tracemalloc

from time import perf_counter

from termcolor import colored


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def log_default(_func=None, *, my_logger: logging.Logger = None):
    """Default logging Decorator."""
    def log_default_info(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # -----------------------------------------------------------------
            # --- Initials.
            # -----------------------------------------------------------------
            logger = my_logger
            if my_logger is None:
                logger = logging.getLogger(func.__name__)

            func_name = func.__name__
            first_args = next(iter(args), None)
            if hasattr(first_args, "__dict__"):  # Is first Argument `self`?
                func_name = "%s.%s" % (first_args.__class__.__name__, func.__name__)

            # -----------------------------------------------------------------
            # --- Logging.
            # -----------------------------------------------------------------
            logger.info(colored(f"***" * 27, "green"))
            logger.info(colored(f"*** INSIDE  `{func_name}`", "green"))

            args_repr =\
                "\n                        ".join([repr(a) for a in args])
            kwargs_repr =\
                "\n                        ".join([f"{k}={v!r}" for k, v in kwargs.items()])

            logger.debug(colored(f"    [--- DUMP ---]   ARGS : {args_repr}", "yellow"))
            logger.debug(colored(f"    [--- DUMP ---] KWARGS : {kwargs_repr}", "yellow"))

            try:
                tracemalloc.start()
                start_time = perf_counter()
                res = func(self, *args, **kwargs)
                return res
            except Exception as exc:
                logger.exception(colored(f"### EXCEPTION in `{func_name}`:\n",
                                         f"                  {type(exc).__name__}\n"
                                         f"                  {str(exc)}", "red", "on_white"))
                raise exc
            else:
                pass
            finally:
                current, peak = tracemalloc.get_traced_memory()
                end_time = perf_counter()
                tracemalloc.stop()

                logger.info(colored(f"*** LEAVING `{func_name}`", "green"))
                logger.info(colored(f"*** MEM USE  : {current / 10**6:.6f} MB", "yellow"))
                logger.info(colored(f"    MEM PEAK : {peak / 10**6:.6f} MB", "yellow"))
                logger.info(colored(f"    TOOK     : {end_time - start_time:.6f} sec", "yellow"))
                logger.info(colored(f"***" * 27, "green"))

        return wrapper

    if _func is None:
        return log_default_info
    else:
        return log_default_info(_func)
