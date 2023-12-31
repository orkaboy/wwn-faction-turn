from typing import Self

from imgui_bundle import imgui

from src.layout_helper import LayoutHelper
from src.location import Location
from src.quality import Quality
from src.style import STYLE
from src.system import QUALITY, AssetPrototype, AssetType, cunning_list, force_list, wealth_list


class Asset:
    def __init__(
        self: Self,
        prototype: AssetPrototype | AssetType,
        owner: str,
        uuid: str,
        loc: Location = None,
    ) -> None:
        """Instantiate Asset object."""
        # Variable stats
        self.desc: str = ""
        self.owner = owner
        self.uuid = uuid
        self.prototype = prototype
        self.hp = 0
        self.loc = loc
        self.qualities: list[Quality] = []
        self.init_from_prototype(prototype)
        # Temporary stats
        self.repair_cost = 1
        self.move_target: Location = None

    def is_initialized(self: Self) -> bool:
        return isinstance(self.prototype, AssetPrototype)

    def init_from_prototype(self: Self, prototype: AssetPrototype) -> None:
        self.prototype = prototype
        if self.is_initialized():
            self.hp = self.max_hp()
            if prototype.stats.qualities:
                self.qualities.extend(prototype.stats.qualities)

    def __repr__(self: Self) -> str:
        if self.is_initialized():
            return self.prototype.strings.name
        return "New Asset"

    def max_hp(self: Self) -> int:
        if self.is_initialized():
            return self.prototype.stats.max_hp
        return 0

    def render_brief(self: Self) -> None:
        """Render a hoverable brief."""
        imgui.text(f"{self}")
        LayoutHelper.add_tooltip(
            f"{self.desc}\n\nLocation: {self.loc}\n\nHP{self.hp}/{self.max_hp()}"
        )

    def render(self: Self, idx: str, locations: list[Location]) -> None:
        """Render asset in GUI."""
        # Handle uninitialized assets
        if not self.is_initialized():
            # Create a combo box for selecting assets of a given type
            if imgui.begin_combo(
                label=f"Select asset type##{idx}",
                preview_value="Asset type",
            ):
                match self.prototype:
                    case AssetType.CUNNING:
                        asset_list = cunning_list()
                    case AssetType.FORCE:
                        asset_list = force_list()
                    case AssetType.WEALTH:
                        asset_list = wealth_list()
                    case _:
                        asset_list = []
                for asset_prototype in asset_list:
                    _, selected = imgui.selectable(
                        label=f"{asset_prototype.strings.name}##{idx}",
                        p_selected=False,
                    )
                    LayoutHelper.add_tooltip(asset_prototype.strings.rules)
                    if selected:
                        self.init_from_prototype(asset_prototype)
                imgui.end_combo()
        else:
            _, self.desc = imgui.input_text_multiline(label=f"Description##{idx}", str=self.desc)
            if imgui.begin_combo(label=f"Location##{self.uuid}", preview_value=f"{self.loc}"):
                for loc in locations:
                    _, selected = imgui.selectable(
                        label=f"{loc}##{loc.uuid}",
                        p_selected=False,
                    )
                    LayoutHelper.add_tooltip(loc.desc)
                    if selected:
                        if self.loc:
                            self.loc.assets.remove(self)
                        self.loc = loc
                        loc.assets.append(self)
                imgui.end_combo()

            _, self.hp = imgui.input_int(label=f"HP##{idx}", v=self.hp)
            imgui.same_line()
            imgui.text(f"/{self.max_hp()}")
            imgui.text_wrapped(f"Damage: {self.prototype.strings.damage_formula}")
            imgui.text_wrapped(f"Counter: {self.prototype.strings.counter_formula}")
            imgui.text_wrapped(self.prototype.strings.rules)
            if self.prototype.stats.upkeep:
                imgui.text(f"Upkeep: {self.prototype.stats.upkeep}")
            # Qualities
            imgui.text("Qualities:")
            if len(self.qualities) > 0:
                rm_quality = -1
                for q_idx, quality in enumerate(self.qualities):
                    imgui.same_line()
                    imgui.text(quality.name)
                    LayoutHelper.add_tooltip(quality.rules)
                    if not quality.persistent:
                        imgui.same_line()
                        STYLE.button_color(STYLE.COL_RED)
                        if imgui.button(f"X##rm_q_{idx}_{q_idx}", size=imgui.ImVec2(16, 20)):
                            rm_quality = q_idx
                        STYLE.pop_color()
                    if q_idx < len(self.qualities) - 1:
                        imgui.same_line()
                if rm_quality >= 0:
                    self.qualities.pop(rm_quality)

            if QUALITY.Stealth not in self.qualities:
                imgui.same_line()
                if imgui.button(f"Add Stealth##{idx}"):
                    self.qualities.append(QUALITY.Stealth)
