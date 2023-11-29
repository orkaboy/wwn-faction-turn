from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from src.app import App
from src.asset import Asset
from src.faction import Faction, MagicLevel
from src.layout_helper import LayoutHelper

# Temp
from src.system import CUNNING, TAGS
from src.tag import Tag


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    def __init__(self: Self, config_data: dict) -> None:
        """Initialize WwnApp object."""
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")

        # TEMP
        self.factions: list[Faction] = [
            Faction("id1", "Dragon Empire", cunning=4, force=8, wealth=6, magic=MagicLevel.MEDIUM),
            Faction("id2", "Tali's Empire", cunning=6, force=5, wealth=5, magic=MagicLevel.MEDIUM),
            Faction("id3", "Shadow Council", cunning=8, force=8, wealth=6, magic=MagicLevel.HIGH),
        ]
        self.factions[0].assets.append(Asset(prototype=CUNNING.Informers, owner="id1"))
        self.factions[0].assets.append(Asset(prototype=CUNNING.Informers, owner="id1"))
        self.factions[1].assets.append(Asset(prototype=CUNNING.Informers, owner="id2"))
        self.factions[2].assets.append(Asset(prototype=CUNNING.PettySeers, owner="id3"))

        self.factions[1].tags.append(Tag(prototype=TAGS.Antimagical))

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        imgui.begin("Factions")

        imgui.set_window_pos("Factions", imgui.ImVec2(5, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        if imgui.button("Add Faction"):
            self.factions.append(
                Faction(ident=uuid4().hex, name="New Faction"),
            )

        rm_faction = -1
        for idx, faction in enumerate(self.factions):
            header_open, visible = imgui.collapsing_header(f"{faction.name}##{idx}", True, flags=32)
            if header_open and visible:
                faction.render(idx)
                # Remove button
                if imgui.button(f"Remove Faction##{idx}"):
                    rm_faction = idx
                LayoutHelper.add_spacer()
        if rm_faction >= 0:
            self.factions.pop(rm_faction)

        imgui.end()
