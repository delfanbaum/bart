from pathlib import Path
from bart.config import BartConfig
from bart.project import BartProject
import typer

from bart.utilites import get_valid_pathname


app = typer.Typer()


@app.command()
def begin(
    project_name: str,
):
    """
    Begin a new project in a <project-name> directory with a
    "00-<project-name>" file in the language specified in your application
    config file (if no config file is found, defaults to a ".txt" extension).

    Note that if you'd like to use spaces in your project name, you need to
    enclose them in quotes, e.g., `bart begin "my great project"`.
    """
    project_dir = Path.cwd() / get_valid_pathname(project_name)
    project = BartProject(project_dir)
    project.begin(project_name)


@app.command()
def config():
    """
    List the Bart config options for the current project/directory (or global
    options, if run outside of a project).
    """
    config = BartConfig()

    print("\nBart configuration:")
    for k, v in vars(config).items():
        print(f"  {k}: {v}")
