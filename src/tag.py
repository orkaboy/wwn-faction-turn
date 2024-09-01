from typing import Self

from imgui_bundle import imgui
from yamlable import YamlAble, yaml_info

from src.layout_helper import LayoutHelper
from src.system.tags import TagPrototype, tags_list


@yaml_info(yaml_tag_ns="wwn")
class Tag(YamlAble):
    def __init__(
        self: Self,
        prototype: TagPrototype | str,
    ) -> None:
        """Initialize Tag object."""
        self.prototype = prototype

    def __to_yaml_dict__(self: Self) -> dict:
        prototype: str = self.prototype.ident if self.prototype else None
        return {
            "prototype": prototype,  # Note: needs to be restored
        }

    def render(self: Self, idx: str) -> None:
        """Render Tag in GUI."""
        if self.prototype is None:
            if imgui.begin_combo(label=f"Select tag type##{idx}", preview_value="Tag type"):
                for tag_prototype in tags_list():
                    _, selected = imgui.selectable(
                        label=f"{tag_prototype.name}##{idx}",
                        p_selected=False,
                    )
                    LayoutHelper.add_tooltip(tag_prototype.rules)
                    if selected:
                        self.prototype = tag_prototype
                imgui.end_combo()
            imgui.same_line()  # For Remove button
        else:
            imgui.text(self.prototype.name)
            imgui.text_wrapped(self.prototype.rules)
