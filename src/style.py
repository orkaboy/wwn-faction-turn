from imgui_bundle import imgui


class STYLE:
    """Static namespace for styling."""

    COL_RED = imgui.ImVec4(0.9, 0.2, 0.1, 1.0)
    COL_GREEN = imgui.ImVec4(0.1, 0.9, 0.2, 1.0)

    @staticmethod
    def button_color(col: imgui.ImVec4) -> None:
        imgui.push_style_color(imgui.Col_.button, col)

    @staticmethod
    def pop_color(num: int = 1) -> None:
        imgui.pop_style_color(num)
