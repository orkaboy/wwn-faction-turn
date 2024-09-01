from typing import Self

from imgui_bundle import imgui
from yamlable import YamlAble, yaml_info


@yaml_info(yaml_tag_ns="wwn")
class Goal(YamlAble):
    def __init__(self: Self, name: str, desc: str, difficulty: int, notes: str = "") -> None:
        self.name = name
        self.desc = desc
        self.difficulty = difficulty
        self.notes = notes

    def render(self: Self, idx: str) -> None:
        """Render the Goal."""
        _, self.name = imgui.input_text(label=f"Name##Goal_{idx}", str=self.name)
        _, self.desc = imgui.input_text_multiline(label=f"Description##Goal_{idx}", str=self.desc)
        _, self.difficulty = imgui.input_int(label=f"Difficulty##Goal_{idx}", v=self.difficulty)
        _, self.notes = imgui.input_text_multiline(label=f"Notes##Goal_{idx}", str=self.notes)

    def __to_yaml_dict__(self: Self) -> dict:
        return {
            "name": self.name,
            "desc": self.desc,
            "difficulty": self.difficulty,
            "notes": self.notes,
        }
