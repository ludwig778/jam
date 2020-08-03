import logging
import logging.config
import sys

from common.context import app_context
from constants.logging import LOGGING_CONFIG
from widgets import MainWindow

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.debug("App initialization...")
    window = MainWindow()
    #window.resize(700, 600)
    window.show()
    exit_code = app_context.app.exec_()
    logger.debug("App stopping...")
    sys.exit(exit_code)
