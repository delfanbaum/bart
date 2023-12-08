from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Literal
from tinydb import TinyDb


DEFAULT_DB_PATH: Path = Path.cwd() / ".bart.json"
DEFAULT_CARDS_DIR: Path = Path.cwd() / "corkboard"
DEFAULT_NOTES_DIR: Path = Path.cwd() / "notes"


class Project:
    """
    Project object for grouping things like documents, metadata, resources,
    manifests, etc.
    """
    def __init__(self,
                 title: str,
                 markup: Literal["text", "asciidoc", "markdown"],
                 auto_add_notes_and_cards: bool = True,
                 number_documents: bool = False):
        """
        A project needs a title and a markup language (mixing languages is not
        currently anticipated)
        """
        self.title: str = title
        self.markup: str = markup
        self.manifest: list[Document] = []
        self.auto_add_notes_and_cards = auto_add_notes_and_cards
        self.number_documents = number_documents  # prepend "01_" or not
        self.db_path: Path = DEFAULT_DB_PATH
        self.db: TinyDb = TinyDb(self.db_path)

    def add_document(self):
        pass

    def rename_document(self):
        pass

    def update_document(self):
        pass

    def remove_document(self):
        pass

    def update_manifest(self):
        pass

    def build(self):
        """
        Compiles the files in the manifest into a document ("target format"
        TBD)
        """
        pass


@dataclass
class Document:
    """
    A document, containing at least a Path to a text file, and optionally other
    data, including Paths to "card" files (which can be used for brief
    descriptions, etc.), notes files, etc.

    The assumption is that all "content" will live in various plain-text files,
    so this object is really just the container that associates that other
    data.
    """
    text_path: Path  # the text file
    id: Optional[int]  # assigned by tinydb
    name: Optional[str]
    status: Optional[str]
    card_path: Optional[Path]
    notes_path: Optional[Path]

    def __post_init__(self):
        """
        TK
        """
        if not self.text_path.is_file():
            self.text_path.touch()

        if not self.name:
            self.name = self.text_path.stem

    def add_card_path(self, card_path: Optional[Path] = None):
        """
        Adds a "card" to be used on the "cork board"

        If a path is given and doesn't already exist, create it.
        """
        if card_path:
            if not card_path.is_file():
                card_path.touch()
        else:
            card_path = (DEFAULT_CARDS_DIR /
                         f"card_for_{self.text_path.name}")

    def add_notes_path(self, card_path: Optional[Path] = None):
        """
        Adds a "card" to be used on the "cork board"

        If a path is given and doesn't already exist, create it.
        """
        if card_path:
            if not card_path.is_file():
                card_path.touch()
        else:
            card_path = (DEFAULT_NOTES_DIR /
                         f"notes_on_{self.text_path.name}")
