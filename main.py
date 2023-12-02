import logging

from config import open_config
from log_init import initialize_logging
from src.wwn_app import WwnApp

logger = logging.getLogger(__name__)


def main() -> None:
    # Read config data from file
    config_data = open_config()
    # Initialize logging
    initialize_logging(config_data)

    logger.debug("Started WWN-faction-turn app")
    # Initialize app and GUI
    app = WwnApp(config_data)
    # Main loop
    while app.is_open():
        app.start_frame()
        app.execute()
        app.end_frame()
    app.close()

    logger.debug("Closed WWN-faction-turn app")


if __name__ == "__main__":
    main()
