import logging

logger = logging.getLogger(__name__)


class Callbacks(object):
    def __init__(self, func_name):
        self.func_name = func_name
        self.funcs = {}

    def register(self, instance, func=None):
        func = func or getattr(instance, self.func_name)
        logger.debug(f"Register {func.__name__} for {instance}")
        self.funcs[instance] = func

    def __call__(self, exclude=None):
        logger.debug(f"Callbacks {self.func_name} called")
        for instance, func in self.funcs.items():
            if instance != exclude:
                logger.debug(f"Callback called for {func.__name__} for {instance}")
                func()


update_callback = Callbacks("update_display")
