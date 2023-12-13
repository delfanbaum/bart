from pathlib import Path
from typing import Literal
from tinydb.storages import JSONStorage  # type: ignore
from tinydb_serialization import SerializationMiddleware  # type: ignore
from tinydb_serialization.serializers import (  # type: ignore
    DateTimeSerializer,
    PathSerializer
)


MARKUP_LANGUAGES = Literal["text", "markdown", "asciidoc"]

DEFAULT_DB_PATH: Path = Path.cwd() / ".bart.json"
DEFAULT_NOTES_DIR: Path = Path.cwd() / "notes"
DEFAULT_STATUS_OPTIONS = Literal["New",
                                 "In Progress",
                                 "In Revision",
                                 "Done"]

# As opposed to writing our own interface, let's add serializers!
_serializer = SerializationMiddleware(JSONStorage)
_serializer.register_serializer(DateTimeSerializer(), "TinyDate")
_serializer.register_serializer(PathSerializer(), "TinyPath")

DEFAULT_SERIALIZER = _serializer
