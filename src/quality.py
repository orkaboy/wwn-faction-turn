from typing import Self


class Quality:
    def __init__(
        self: Self,
        name: str,
        ident: str,
    ) -> None:
        """Instantiate Quality object."""
        self.name = name
        self.id = ident
