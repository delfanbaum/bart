class TestProjectSetup:

    def test_can_create_project_from_empty_directory(self):
        pass

    def test_can_create_project_from_nonempty_directory(self):
        pass

    def test_project_has_expected_attrs(self):
        """ title, markup language, etc. """
        pass

    def test_can_add_existing_documents_to_project_on_creation(self):
        pass

    def test_can_add_existing_documents_to_project_from_glob_notation(self):
        """
        For example, I want to say add all "*.adoc" files to my project
        """
        pass

    def test_can_set_up_notes_and_cards_automatically(self):
        pass

    def test_can_set_up_notes_manually(self):
        pass

    def test_can_generate_scaffold_of_n_documents(self):
        pass

    def test_can_save_project_to_json(self):
        pass


class TestDatabaseFunctions:
    """
new project creates database
updates to project data updates database
new [document, cards, notes] path is inserted into database
update to [document, cards, notes] is updated in database
    """
    pass


class TestDocument:

    def test_can_create_document(self):
        pass

    def test_has_expected_attrs(self):
        pass

    def test_can_update_document_path(self):
        pass

    def test_can_rename_document_path(self):
        pass

    def test_can_raname_document(self):
        pass

    def test_can_update_card_path(self):
        pass

    def test_can_update_notes_path(self):
        pass

    def test_can_update_title(self):
        pass
