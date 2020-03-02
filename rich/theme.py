import configparser
from typing import Dict, IO

from .default_styles import DEFAULT_STYLES
from .style import Style


class Theme:
    """An container for style information, used by :class:`~rich.console.Console`.
    
    Args:
        styles (Dict[str, Style], optional): A mapping of style names on to styles. Defaults to None for empty styles.
        inherit (bool, optional): Switch to inherit default styles. Defaults to True.
    """

    def __init__(self, styles: Dict[str, Style] = None, inherit: bool = True):
        if inherit:
            self.styles = DEFAULT_STYLES
        else:
            self.styles = {}
        if styles is not None:
            self.styles.update(styles)

    @property
    def config(self) -> str:
        """Get contents of a config file for this theme."""
        config_lines = ["[styles]"]
        append = config_lines.append
        for name, style in sorted(self.styles.items()):
            append(f"{name} = {style}")
        config = "\n".join(config_lines)
        return config

    @classmethod
    def from_file(
        cls, config_file: IO[str], source: str = None, inherit: bool = True
    ) -> "Theme":
        """Load a theme from a text mode file.

        Args:
            config_file (IO[str]): An open conf file.
            source (str, optional): The filename of the open file. Defaults to None.
            inherit (bool, optional): Switch to inherit default styles. Defaults to True. 
        
        Returns:
            Theme: A New theme instance.
        """
        config = configparser.ConfigParser()
        config.read_file(config_file, source=source)
        styles = {name: Style.parse(value) for name, value in config.items("styles")}
        theme = Theme(styles, inherit=inherit)
        return theme

    @classmethod
    def read(cls, path: str, inherit: bool = True) -> "Theme":
        """Read a theme from a path.

        Args:
            path (str): Path to a config file readable by Python configparser module.            
            inherit (bool, optional): Switch to inherit default styles. Defaults to True. 
        
        Returns:
            Theme: A new theme instance.
        """
        with open(path, "rt") as config_file:
            return cls.from_file(config_file, source=path, inherit=inherit)
