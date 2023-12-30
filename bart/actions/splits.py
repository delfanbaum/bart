from enum import Enum
from pathlib import Path


class Markup(Enum):
    TEXT = ".txt"
    MARKDOWN = ".md"
    ASCIIDOC = ".adoc"


class MarkupNotAllowedException(Exception):
    pass


def get_delimiter(file: Path):
    """
    TODO: allow users to config their own delimiters per filetype
    """
    match file.suffix:
        case Markup.MARKDOWN.value:
            return "#"
        case Markup.ASCIIDOC.value:
            return "="
        case _:
            raise MarkupNotAllowedException(
                    "This operation is not available for this type of markup.")


def get_numbering(file: Path):
    """
    TODO: handle two- three- four-digit numbering more elegantly
    """
    try:
        return int(file.name.split('-')[0])
    except ValueError:
        return 0


def get_valid_filename(name) -> str:
    """
    TODO: handle commas, colons, etc.
    """
    s = str(name).strip().replace(' ', '-')
    return s.lower()


def write_split(split_lines: list,
                delimeter: str,
                numbering: int,
                suffix: str) -> int:
    section_title = split_lines[0].split(delimeter)[-1]
    text = "".join(split_lines)
    out_fn = str(numbering) + "-" + get_valid_filename(section_title) + suffix

    with open(out_fn, 'wt') as f:
        print(f"Writing {out_fn}...")
        f.write(text)

    return numbering + 1


def split_at_headings(fn):
    file = Path(fn)
    delimeter = get_delimiter(file)
    numbering = get_numbering(file)
    current_split = []

    with file.open('rt') as f:
        text_lines = f.readlines()

    for num, line in enumerate(text_lines):
        # next heading
        if line.find(delimeter) == 0 and text_lines[num+1] == "\n":
            if current_split:
                numbering = write_split(current_split,
                                        delimeter,
                                        numbering,
                                        file.suffix)

            current_split = [line]
        else:
            current_split.append(line)

    # write final split
    write_split(current_split, delimeter, numbering, file.suffix)
