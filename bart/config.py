from pathlib import Path

import tomlkit
import typer

PROJECT_CONFIG_PATH = Path.cwd() / '.bart.toml'

# possible config locations, ordered in terms of priority
BART_CONFIG_PATHS = [
    Path.home() / ".config/bart/bart.toml",
    Path(typer.get_app_dir("bart")),
]


class BartConfig:
    """
    Project and global config, with defaults
    """

    def __init__(self, project_dir: Path = Path.cwd()) -> None:
        """
        Sets default values, looks for and pulls in any user or project
        configuration overrides
        """

        # defaults
        self.markup = "asciidoc"
        self.markup_ext= "adoc"
        self.doc_numbering = 1  # i.e., 00, 01, 02
        self.default_converter = "asciidoc" # i.e., asciidoc.py
        self.default_build = "html"

        # user config
        for config in BART_CONFIG_PATHS:
            if config.is_file():
                self.extend(config)

        # project config
        if (project_dir / '.bart.toml').is_file():
            self.extend(project_dir / '.bart.toml')


    def extend(self, config: Path):
        """
        Extends the config with a TOML config file, overriding anything
        previously configured (i.e., defaults).
        """
        with config.open("rt") as f:
            _config = tomlkit.parse(f.read())
            for k, v in _config.get('bart', {}).items():
                self.__dict__[k] = v

    def write_to(self, destination: Path):
        """
        Handy way to write the default configs out for user adjustment
        """
        toml_config = tomlkit.document()

        config_values = tomlkit.table()
        for k, v in vars(self).items():
            config_values.add(k, v)

        toml_config.add("bart", config_values)

        with destination.open("wt") as f:
            f.write(tomlkit.dumps(toml_config))
