"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from ddcore.logconst import *


# =============================================================================
# ===
# === COMMON
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Log Keys.
# -----------------------------------------------------------------------------
LOG_KEY_ABS_ENV = "abs_env"
LOG_KEY_ABS_EXEC_TIME = "abs_exec_time"
LOG_KEY_ABS_MEM_USAGE = "abs_mem_usage"
LOG_KEY_ABS_MEM_PEAK = "abs_mem_peak"

LOG_KEY_NEW_RELIC_APP_NAME = "new_relic_app_name"

LOG_KEY_STATUS = "status"

# -----------------------------------------------------------------------------
# --- Log Values.
# -----------------------------------------------------------------------------
LOG_VAL_TYPE_API_REQUEST = "API_REQUEST"
LOG_VAL_TYPE_DAEMON_REQUEST = "DAEMON_REQUEST"
LOG_VAL_TYPE_DB_ERROR = "DB_ERROR"
LOG_VAL_TYPE_EXCEPTION = "EXCEPTION"
LOG_VAL_TYPE_FUNC_CALL = "FUNC_CALL"
LOG_VAL_TYPE_FRONT_END_REQUEST = "FRONT_END_REQUEST"
LOG_VAL_TYPE_OUTAGE = "OUTAGE"