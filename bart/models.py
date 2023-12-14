from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .settings import (
    DEFAULT_STATUS_OPTIONS,
    MARKUP_LANGUAGES
)


@dataclass
class Document:
    """
    A document, containing at least a Path to a text file, and optionally other
    data. The "card" is kept with the document in the DB (since I wouldn't
    expect those to be edited directly, since they'll only be useful in a
    view).
    """
    text_path: Path  # the text file
    id: Optional[int] = None  # assigned by tinydb
    name: Optional[str] = None
    card: Optional[str] = None
    status: DEFAULT_STATUS_OPTIONS = "New"  # user-defined later
    word_count_tracker: dict[str, int] = field(
                default_factory=lambda: {
                    datetime.today().strftime("%Y-%m-%d"): 0
                    })

    def __post_init__(self):
        """
        Creates a file if there is not one there already, adds a name to the
        file if it doesn't already have one.
        """
        if not self.text_path.is_file():
            self.text_path.touch()

        if not self.name:
            self.name = self.text_path.stem


@dataclass
class Project:
    """
    Project object for grouping things like documents, metadata, resources,
    manifests, etc.
    """
    name: str
    markup_language: MARKUP_LANGUAGES
    title: Optional[str] = None
    manifest: list[int] = field(default_factory=list)  # document IDs
    number_documents: bool = False  # option to prepend "01_"
    last_update: datetime = datetime.now()
    word_count_tracker: dict[str, int] = field(
                default_factory=lambda: {
                    datetime.today().strftime("%Y-%m-%d"): 0
                    })
