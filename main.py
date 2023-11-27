from config import open_config
from log_init import initialize_logging


def main() -> None:
    # Read config data from file
    config_data = open_config()
    initialize_logging(config_data)


if __name__ == "__main__":
    main()
