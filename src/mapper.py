from collections.abc import Callable


def get_class_values(Class: Callable) -> list:
    """
    Return a list of class attribute values of arbitrary type.

    For example:
    ```
    class TAGS:
        Supported = Supported()
        Zealot = Zealot()
        ...

    tags = get_class_values(TAGS))
    ```
    """
    return [v for k, v in vars(Class).items() if not k.startswith("__")]
