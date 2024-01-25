from typing import Optional
from pathlib import Path

import tomlkit
import typer

PROJECT_CONFIG_PATH = Path.cwd() / '.bart.toml'


class BartConfig:
    """
    Project and global config, with defaults
    """

    def __init__(self, toml_config: Optional[dict] = None):

        # defaults
        self.markup = "asciidoc"
        self.doc_numbering = 1  # i.e., 00, 01, 02
        self.default_converter = "asciidoc" # i.e., asciidoc.py
        self.default_build = "html"

        match self.markup:
            case "asciidoc":
                self.project_extension = "adoc"
            case "markdown":
                self.project_extension = "md"

        # user-specific overrides
        if toml_config:
            for k, v in toml_config.items():
                self[k] = v


    def extend_with(self, toml_config: dict):
        for k, v in toml_config.items():
            self[k] = v

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


def get_config_path() -> Optional[Path]:
    """
    Looks for app configuration in the expected places, and if it can't
    find them, it notifies the user and exits
    """
    
    # possible config locations, ordered in terms of priority
    default_configs = [
        Path.home() / ".config/bart/bart.toml",
        Path(typer.get_app_dir("bart")),
    ]

    for config in default_configs:
        if config.is_file():
            return config.parent


def get_config() -> BartConfig:
    """
    Reads the global bart config
    """
    config_path = get_config_path()
    
    if config_path:
        with config_path.open("rt") as f:
            bart_config = BartConfig(tomlkit.parse(f.read()))

    else:
        bart_config = BartConfig()

    if PROJECT_CONFIG_PATH.exists():
        with PROJECT_CONFIG_PATH.open('rt') as f:
            project_config = tomlkit.parse(f.read())

        bart_config.extend_with(project_config)

    return bart_config


def write_default_config(config_path: Path):
    """
    Writes the config to the config path
    """
    defaults = BartConfig()

    config = tomlkit.document()

    config_options = tomlkit.table()
    for k, v in vars(defaults).items():
        config_options.add(k, v)

    config.add("bart", config_options)

    with config_path.open("wt") as f:
        f.write(tomlkit.dumps(config))
