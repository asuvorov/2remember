"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""


class PlatformCode:
    """Platform Code."""

    # =========================================================================
    # === Informational Responses (1000 - 1999).
    PLATFORM_CODE_MISSING = 1000

    # =========================================================================
    # === Successful Responses (2000 - 2999).
    SUCCESS = 2000

    # =========================================================================
    # === Redirection Messages (3000 - 3999).

    # =========================================================================
    # === Client Error Responses (4000 - 4999).

    # =========================================================================
    # === Server Error Messages (5000 - 5999).

    # =========================================================================
    # === Data Exceptions (5000 - 5999).
    MISSING_MAND_PARAM = 5000
    INVALID_PARAM_VAL = 5001
    INVALID_PATH = 5002
    INVALID_UUID = 5003
    INVALID_INPUT = 5004
    INVALID_XML = 5005
    INVALID_JSON = 5006
    DATA_NOT_FOUND = 5007
    INVALID_TOKEN = 5008
    DATA_LIMIT_REACHED = 5009

    # =========================================================================
    # === HTTP Exceptions (6000 - 6999).
    INVALID_URL = 6000
    INVALID_REQUEST = 6001
    HTTP_SERVER_ERROR = 6003
    BLOCKED_CLIENT_IP = 6008
    BLOCKED_CLIENT_AGENT = 6009
    NETWORK_CONNECT_TIMEOUT_ERROR = 6013
    IP_ADDRESS_BLOCKED = 6016

    # =========================================================================
    # === DB Exceptions (7000 - 7999).
    DB_CONNECTION_ERROR = 7000
    DB_OPERATIONAL_ERROR = 7001
    DB_ERROR = 7002

    # =========================================================================
    # === Server Exceptions (9000 - 9999).
    SERVER_ERROR = 9000

    # =========================================================================
    # === Memcached Exceptions (10000 - 10499).
    MEMCACHED_INIT_ERROR = 10000
    MEMCACHED_SET_ERROR = 10001
    MEMCACHED_GET_ERROR = 10002
    MEMCACHED_DELETE_ERROR = 10003

    # =========================================================================
    # === Redis Exceptions (10500 - 10699).
    REDIS_CONNECTION_ERROR = 10500
    REDIS_INTERNAL_ERROR = 10501
    REDIS_RESPONSE_ERROR = 10502

    # =========================================================================
    # === SQS Exceptions (10700 - 10899).
    SQS_CLIENT_CONNECTION_ERROR = 10700
    SQS_INTERNAL_ERROR = 10701

    # =========================================================================
    # === S3 Exceptions (10900 - 10999).
    S3_CLIENT_CONNECTION_ERROR = 10900
