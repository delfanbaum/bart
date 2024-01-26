from enum import Enum
from pathlib import Path

import tomlkit
import typer

PROJECT_CONFIG_PATH = Path.cwd() / '.bart.toml'

# possible config locations, ordered in terms of priority
BART_CONFIG_PATHS = [
    Path.home() / ".config/bart/bart.toml",
    Path(typer.get_app_dir("bart")),
]


class MarkupLanguages(Enum):
    """
    Supported languages; the value is the markup extension
    """
    ASCIIDOC = "adoc"
    MARKDOWN = "md"
    TEXT = "txt"

    def extension(self):
        return self.value


class DocConverers(Enum):
    """
    Supported language-> html converters

    (Note that asciidoctor and pandoc are subprocesses)
    """

    ASCIIDOC = "asciidoc"
    ASCIIDOCTOR = "asciidoctor"
    MARKDOWN2 = "markdown"
    PANDOC = "pandoc"

class BuildFormats(Enum):
    """
    Post-HTML conversion targets; values are required external dependencies
    """
    HTML = None
    PDF_WP = "weasyprint"
    PDF_PJS = "pagedjs-cli"
    DOC = "pandoc"
    DOCX = "pandoc"



class BartConfig:
    """
    Project and global config, with defaults
    """

    def __init__(self, project_dir: Path = Path.cwd(), use_default: bool = False) -> None:
        """
        Sets default values, looks for and pulls in any user or project
        configuration overrides
        """

        # defaults
        self.markup = MarkupLanguages.ASCIIDOC
        self.default_converter = DocConverers.ASCIIDOC
        self.default_build = BuildFormats.HTML
        self.doc_levels = 1  # how many "deep" the tree goes 1-indexed

        if not use_default:
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
        previously configured (i.e., defaults) if the type/value is
        acceptable
        """
        with config.open("rt") as f:
            _config = tomlkit.parse(f.read())

            for k, v in _config.get('bart', {}).items():
                match k:
                    case "markup" if v.upper() in [m.name for m in
                                           MarkupLanguages]:
                            self.markup = MarkupLanguages[v.upper()]

                    case "default_converter" if v.upper() in [b.name for b in
                                                  DocConverers]:
                        self.default_build = DocConverers[v.upper()]

                    case "default_build" if v.upper() in [b.name for b in
                                                  BuildFormats]:
                        self.default_build = BuildFormats[v.upper()]

                    case "doc_levels" if (isinstance(v, int) and v > 0):
                        self.doc_levels = v
                

    def write_to(self, destination: Path):
        """
        Handy way to write the default configs out for user adjustment
        """
        toml_config = tomlkit.document()

        config_values = tomlkit.table()
        for k, v in vars(self).items():
            if isinstance(v, Enum):
                config_values.add(k, v.name.lower())
            else:
                config_values.add(k, v)

        toml_config.add("bart", config_values)

        with destination.open("wt") as f:
            f.write(tomlkit.dumps(toml_config))
