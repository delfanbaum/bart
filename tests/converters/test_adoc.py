from bart.converters.adoc import process_with_asciidoctor


def test_process_asciidoctor():
    result = process_with_asciidoctor('This is a _test_')
    assert "<p>This is a <em>test</em></p>" in result
