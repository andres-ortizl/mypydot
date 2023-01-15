import pytermgui as ptg
from dataclasses import dataclass

PALETTE_BLUE = "#9fd7ef"
PALETTE_PURPLE = "#ef9fd7"
GRADIENT_PURPLE = "[!gradient(105)]"
GRADIENT_GREEN = "[!gradient(83)]"
HIGHLIGHT = "@secondary dim #auto"
LABEL = "@surface dim #auto"
SUCCESS_LABEL = "@success dim #auto"


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

    # Container Styles
    ptg.Container.styles.border__corner = PALETTE_BLUE

    # Window Styles
    ptg.Window.styles.border__corner = PALETTE_BLUE

    # Button Styles
    ptg.Button.styles.highlight = HIGHLIGHT
    ptg.Button.styles.label = LABEL
