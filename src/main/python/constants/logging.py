LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'default': { 
            'format': '%(module)20s %(funcName)-25s %(levelname)s %(message)s'
        },
    },
    'handlers': { 
        'console': { 
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler'
        }
    },
    # [DEBUG, INFO, ERROR, WARNING, CRITICAL]
    'loggers': {
        'testetsets': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'api.chord_progression': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'widgets.sequencer': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'widgets.player': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'widgets.instruments': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'api.instruments': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}