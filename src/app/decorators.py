"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import sys, os, functools
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def log_default(_func=None):
    def log_default_info(func):
        @functools.wraps(func)
        def log_default_wrapper(self, *args, **kwargs):
            """Build logger object"""
            logger_obj = log.get_logger(
                log_file_name=self.log_file_name,
                log_sub_dir=self.log_file_dir)

            """log function begining"""
            logger_obj.info("Begin function")

            try:
                """ log return value from the function """
                value = func(self, *args, **kwargs)
                logger_obj.info(f"Returned: - End function {value!r}")
            except:
                """log exception if occurs in function"""
                logger_obj.error(f"Exception: {str(sys.exc_info()[1])}")

                raise

            return value

        return log_default_wrapper

    if _func is None:
        return log_default_info
    else:
        return log_default_info(_func)
