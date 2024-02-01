from bart.actions.joins import join_docs


class TestJoins:
    """
    Tests various "join" operations, which include both joining docs in memory
    (e.g., for building), as well as joining docs to save them into one (using
    tags or comments to preserve previous filenames, depending on markup).
    """

    def test_join_documents_memory(self, test_project_adoc):
        """
        We do a simple "add these document texts together" operation
        """

        ch1, ch2 = test_project_adoc.get_project_docs()[1:3]
        text = join_docs([ch1, ch2])
        assert "= Chapter One\n" in text
        assert "= Chapter Two\n" in text

    def test_join_documents_with_tags(self, test_project_adoc):
        """
        If the documents are asciidoc, we can optionally delimit them with
        tags denoting their source filenames
        """
        ch1, ch2 = test_project_adoc.get_project_docs()[1:3]
        text = join_docs([ch1, ch2], True)
        for ch in [ch1, ch2]:
            assert f"\n# tag::{ch.name}[]\n" in text
            assert f"\n# end::{ch.name}[]\n" in text


    def test_join_documents_with_comments(self, test_project_md):
        """
        If the documents are markdown, we can optionally delimit them with
        comments denoting their source filenames
        """
        ch1, ch2 = test_project_md.get_project_docs()[1:3]
        text = join_docs([ch1, ch2], True)
        for ch in [ch1, ch2]:
            assert f"\n<!-- {ch.name} -->\n" in text
            assert f"\n<!-- end {ch.name} -->\n" in text

    def test_join_writes_and_reorders_two_docs(self, test_project_md):
        """
        Optionally, the join should be "permanent", reordering the docs in the
        project and preserving the delimiters (if not delimiters, no perm join)
        """
        start_length = len(test_project_md.documents)
        ch1, ch2 = test_project_md.get_project_docs()[1:3]
        _ = join_docs([ch1, ch2], delimit=True, write=True)
        assert len(test_project_md.get_project_docs()) == start_length - 1
        assert ch2 not in test_project_md.documents
        # check renames
        for i, d in enumerate(test_project_md.documents):
            assert str(i) in d.name[:3]

    def test_join_writes_and_reorders_many_docs(self, test_project_md):
        """
        Optionally, the join should be "permanent", reordering the docs in the
        project and preserving the delimiters (if not delimiters, no perm join)
        """
        _ = join_docs(test_project_md.get_project_docs()[1:],
                      delimit=True,
                      write=True)
        assert len(test_project_md.get_project_docs()) == 2
        assert test_project_md.documents[1].name[:3] == "01-"
