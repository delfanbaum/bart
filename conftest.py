from bart.models import Project
import pytest


@pytest.fixture(scope="class")
def fresh_project(tmp_path_factory):
    """ a project that starts empty to be used within a test class """
    db = tmp_path_factory.mktemp("tests") / ".bart.json"
    empty_project = Project(
            title="Empty Test Project",
            markup="text",
            db_path=db
            )
    yield empty_project
