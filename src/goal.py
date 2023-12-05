from typing import Self

from imgui_bundle import imgui


class Goal:
    def __init__(self: Self, name: str, desc: str, difficulty: int) -> None:
        self.name = name
        self.desc = desc
        self.difficulty = difficulty
        self.notes = ""

    def render(self: Self, idx: str) -> None:
        """Render the Goal."""
        _, self.name = imgui.input_text(label=f"Name##Goal_{idx}", str=self.name)
        _, self.desc = imgui.input_text_multiline(label=f"Description##Goal_{idx}", str=self.desc)
        _, self.difficulty = imgui.input_int(label=f"Difficulty##Goal_{idx}", v=self.difficulty)
        _, self.notes = imgui.input_text_multiline(label=f"Notes##Goal_{idx}", str=self.notes)
