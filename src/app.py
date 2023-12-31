"""
GUI Module.

Responsible for setting up the GUI window using glfw, and handling the
backend side of imgui rendering and event polling.
"""

import ctypes
import logging
import sys
from typing import Any, Self

import glfw
import OpenGL.GL as gl
from imgui_bundle import imgui

from src.layout_helper import LayoutHelper

logger = logging.getLogger(__name__)


# Create the window that our GUI/visualization will be in
def create_glfw_window(
    title: str,
    width: int,
    height: int,
) -> Any:  # noqa: ANN401
    """Initialize the glfw window and OpenGL context."""
    if not glfw.init():
        logger.error("Could not initialize OpenGL context")
        sys.exit(1)

    # Set up OpenGL
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        width=int(width),
        height=int(height),
        title=title,
        monitor=None,
        share=None,
    )
    glfw.make_context_current(window)

    # Check we actually managed to create a window
    if not window:
        glfw.terminate()
        logger.error("Could not initialize glfw window")
        sys.exit(1)

    return window


class App:
    """Class to handle the top level GUI window."""

    def __init__(self: Self, config_data: dict, title: str) -> None:
        """Initialize App object and create imgui window."""
        super().__init__()

        config_ui: dict = config_data.get("ui", {})
        width = config_ui.get("width", 480)
        height = config_ui.get("height", 800)

        self.background_color = (0, 0, 0, 1)

        # Create Window/Context and set up renderer
        self.window = create_glfw_window(title=title, width=width, height=height)
        gl.glClearColor(*self.background_color)
        imgui.create_context()

        self.io = imgui.get_io()
        self.io.config_flags |= imgui.ConfigFlags_.nav_enable_keyboard
        self.io.config_flags |= imgui.ConfigFlags_.docking_enable

        self.io.fonts.add_font_from_file_ttf(
            filename="assets/fonts/FiraSans-Regular.ttf", size_pixels=16
        )

        gui_rounding = 3
        imgui.get_style().frame_rounding = gui_rounding
        imgui.get_style().window_rounding = gui_rounding
        imgui.get_style().popup_rounding = gui_rounding
        imgui.get_style().child_rounding = gui_rounding
        imgui.get_style().tab_rounding = gui_rounding
        imgui.get_style().scrollbar_rounding = gui_rounding
        imgui.get_style().grab_rounding = gui_rounding
        imgui.get_style().scrollbar_size = 12

        color_background = imgui.ImVec4(0.08, 0.11, 0.16, 1.00)
        color_primary = imgui.ImVec4(0.05, 0.25, 0.43, 1.00)
        color_primary_light = imgui.ImVec4(0.13, 0.75, 1.00, 1.00)
        color_primary_dark = imgui.ImVec4(0.05, 0.05, 0.08, 1.00)
        LayoutHelper.set_gui_color("window_bg", color_background)
        LayoutHelper.set_gui_color("button", color_primary)
        LayoutHelper.set_gui_color("button_active", color_primary_dark)
        LayoutHelper.set_gui_color("button_hovered", color_primary_light)
        LayoutHelper.set_gui_color("header", color_primary)
        LayoutHelper.set_gui_color("header_hovered", color_primary_light)
        LayoutHelper.set_gui_color("tab", color_primary_dark)
        LayoutHelper.set_gui_color("tab_active", color_primary)
        LayoutHelper.set_gui_color("tab_hovered", color_primary_light)
        LayoutHelper.set_gui_color("tab_unfocused", color_primary_dark)
        LayoutHelper.set_gui_color("tab_unfocused_active", color_primary)
        LayoutHelper.set_gui_color("frame_bg", color_primary_dark)
        LayoutHelper.set_gui_color("check_mark", color_primary_light)
        LayoutHelper.set_gui_color("slider_grab", color_primary_light)
        LayoutHelper.set_gui_color("title_bg_active", color_primary_light)

        vsync: bool = config_ui.get("vsync", True)
        glfw.swap_interval(1 if vsync else 0)

        # Setup Platform/Renderer backends

        # You need to transfer the window address to imgui.backends.glfw_init_for_opengl
        # proceed as shown below to get it.
        glsl_version = "#version 150"
        window_address = ctypes.cast(self.window, ctypes.c_void_p).value
        imgui.backends.glfw_init_for_opengl(window_address, True)
        imgui.backends.opengl3_init(glsl_version)

    def is_open(self: Self) -> bool:
        """Return True while the GUI window is open. Return False if the user quits the program."""
        return not glfw.window_should_close(self.window)

    def start_frame(self: Self) -> None:
        """Call at start of frame to handle imgui setup, memory readout and event polling."""
        glfw.poll_events()
        imgui.backends.opengl3_new_frame()
        imgui.backends.glfw_new_frame()
        imgui.new_frame()

    def execute(self: Self) -> None:
        """Override."""
        pass

    def end_frame(self: Self) -> None:
        """Finalize drawing. Should be called at the end of each frame."""
        imgui.render()

        gl.glClearColor(*self.background_color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.backends.opengl3_render_draw_data(imgui.get_draw_data())
        glfw.swap_buffers(self.window)

    def close(self: Self) -> None:
        """Cleanup imgui and cleanly close down glfw."""
        imgui.backends.opengl3_shutdown()
        imgui.backends.glfw_shutdown()
        imgui.destroy_context()

        glfw.destroy_window(self.window)
        glfw.terminate()
