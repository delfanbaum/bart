from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Collapsible, Header, Footer, Static, Input, TextArea


class OutlineElement(Static):
    """
    An outline element
    """

    def compose(self) -> ComposeResult:
        """
        A title and a text area
        """
        with Collapsible(collapsed=True):
            yield Input(placeholder="Section title here...")
            yield TextArea()


class OutlineApp(App):
    """
    Proof of concept "outline" feature
    """

    BINDINGS = []

    def compose(self) -> ComposeResult:
        """ Creates child widgets """
        yield Header()
        yield ScrollableContainer(
                OutlineElement(),
                OutlineElement(),
                )
        yield Footer()


if __name__ == "__main__":
    app = OutlineApp()
    app.run()
