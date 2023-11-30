"""
GUI Module.

Responsible for setting up the GUI window using glfw, and handling the
backend side of imgui rendering and event polling.
"""

import logging

from imgui_bundle import imgui

logger = logging.getLogger(__name__)


class LayoutHelper:
    """
    Provides helper functions for creating GUI elements.

    ```py
    add_spacer()             # Add a horizontal line with some padding.
    add_spacings(n)          # Add n imgui.spacing() elements.
    add_tooltip(text, width) # Add a tooltip to the previous element.
    ```
    """

    @staticmethod
    def add_spacer(separator: int = 1) -> None:
        """Add a horizontal line with some padding."""
        imgui.spacing()
        for _ in range(separator):
            imgui.separator()
        imgui.spacing()

    @staticmethod
    def add_spacings(n: int = 2) -> None:
        """Add multiple imgui.spacing() at once."""
        for _ in range(n):
            imgui.spacing()

    @staticmethod
    def add_tooltip(text: str, width: int = 300) -> None:
        """
        Add a tooltip to the previous element.

        Set `width` to `-1` to disable automatic text wrapping.
        """
        if imgui.is_item_hovered(flags=imgui.HoveredFlags_.delay_normal) and imgui.begin_tooltip():
            imgui.set_next_window_size(size=imgui.ImVec2(0.0, 0.0))  # auto-fit tooltip to content
            imgui.push_text_wrap_pos(width)
            imgui.text_unformatted(text)
            imgui.pop_text_wrap_pos()
            imgui.end_tooltip()

    @staticmethod
    def set_gui_color(ui_element: str, color: imgui.ImVec4) -> None:
        """
        Set the color of a GUI element.

        Args:
        ----
            ui_element: Check the demo window for valid values
            color: Tuple of (r, g, b, a) values.
        """
        ui_element = getattr(imgui.Col_, ui_element)
        imgui.get_style().set_color_(ui_element, color)
