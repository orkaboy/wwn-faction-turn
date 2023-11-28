from config import open_config
from log_init import initialize_logging
from src.app import App


def main() -> None:
    # Read config data from file
    config_data = open_config()
    # Initialize logging
    initialize_logging(config_data)
    # Initialize app and GUI
    app = App(config_data)
    # Main loop
    while app.is_open():
        app.start_frame()
        app.end_frame()
    app.close()


if __name__ == "__main__":
    main()
