import pytermgui as ptg
from dataclasses import dataclass

PALETTE_LIGHT = "#FCBA03"
PALETTE_MID = "#8C6701"
PALETTE_BLUE = "#9fd7ef"
PALETTE_PURPLE = "#ef9fd7"
GRADIENT_PURPLE = "[!gradient(105)]"
GRADIENT_GREEN = "[!gradient(83)]"


@dataclass
class Style:

    @staticmethod
    def configure_widgets() -> None:
        """Defines all the global widget configurations.
    Some example lines you could use here:
        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    ptg.boxes.ROUNDED.set_chars_of(ptg.Window)
    ptg.boxes.ROUNDED.set_chars_of(ptg.Container)

    # ptg.Button.styles.label = "app.button.label"
    # ptg.Button.styles.highlight = "app.button.highlight"

    ptg.Slider.styles.filled__cursor = PALETTE_MID
    ptg.Slider.styles.filled_selected = PALETTE_LIGHT
    ptg.Window.styles.border__corner = PALETTE_BLUE
    # ptg.Container.styles.border__corner = "[!gradient(83)]"
    ptg.Container.styles.border__corner = PALETTE_BLUE
    ptg.Splitter.set_char("separator", "")
