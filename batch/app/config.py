import logging
import os

# ------------------------------------------
# ログ設定
# ------------------------------------------
# ログレベル判定
log_level = logging.INFO
if bool(os.environ.get("LOG_DEBUG_FLG", False)):
    log_level = logging.DEBUG

LOG = {
    'version': 1,
    # フォーマット設定
    'formatters': {
        'customFormat': {
            'format': '%(asctime)s %(name)s [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    # ハンドラー設定
    'handlers': {
        'customStreamHandler': {
            'class': 'logging.StreamHandler',
            'formatter': 'customFormat',
            'level': log_level
        },
    },
    # ロガー対象一覧
    'root': {
        'handlers': ['customStreamHandler'],
        'level': log_level,
    },
    'loggers': {
        'bin': {
            'handlers': ['customStreamHandler'],
            'level': log_level,
            'propagate': False
        },
    }
}

# ------------------------------------------
# sentry設定
# ------------------------------------------
SENTRY = {
    "url": os.environ.get("SENTRY_URL")
}

# ------------------------------------------
# slack設定
# ------------------------------------------
SLACK = {
    "url": os.environ.get("SLACK_URL")
}

# ------------------------------------------
# Facebook設定
# ------------------------------------------
FB = {
    "user_id": os.environ.get("FB_USER_ID"),
    "password": os.environ.get("FB_PASSWORD"),
}

