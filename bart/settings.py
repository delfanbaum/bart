from enum import Enum
from pathlib import Path


class KnownMarkup(Enum):
    TEXT = ".txt"
    MARKDOWN = ".md"
    ASCIIDOC = ".adoc"


DEFAULT_CONFIG_PATHS = [
    Path("~/.config/bart/bart.toml")
    ]
