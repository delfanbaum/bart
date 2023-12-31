from pathlib import Path
from typing import Annotated
from bart.templates import project_root_template
from bart.utilites import get_valid_pathname
import typer


app = typer.Typer()


@app.command()
def begin(
    project_name: str,
    use_current_directory: Annotated[
        bool, typer.Option(help="Begin your project in the current directory")
    ] = False,
):
    """
    Begin a new project in a <project-name> directory with a
    "00-<project-name>" file in the language specified in your application
    config file (if no config file is found, defaults to a ".txt" extension).
    """
    if use_current_directory:
        project_dir = Path.cwd() / get_valid_pathname(project_name)
        project_dir.mkdir()

    else:
        project_dir = Path.cwd()

    project_root_file = project_dir / f"00-{project_name}.txt"

    with project_root_file.open('wt') as f:
        f.write(project_root_template(project_name))
