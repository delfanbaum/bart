import subprocess


def process_with_asciidoctor(text):
    """
    Converts asciidoc to html via asciidoctor (ruby)
    """
    with open('tmp.adoc', 'wt') as f:
        f.write_through
    result = subprocess.run(['asciidoctor', '-a', "stylesheet!",
                             "-o", "-", "-"],
                            input=text,
                            capture_output=True,
                            text=True)

    if result.stderr == '':
        return result.stdout

    else:
        print(f'\nError in Asciidoctor conversion: {result.stderr}')
        print("Exiting...")
        exit()


def process_with_python_asciidoc(fn):
    result = subprocess.run(['asciidoc', '-b', 'html5', '-a', 'linkcss',
                             '-a', 'disable-javascript', "-o", "-", fn],
                            capture_output=True,
                            text=True)
    if result.returncode == 0:
        html = result.stdout
        # remove linked stylesheet....
        html = html.replace(
            '<link rel="stylesheet" href="./asciidoc.css" type="text/css">', ''
            )
        return html

    else:
        print()
        print(f'Error code {result.returncode}: {result.stderr}')
        exit()
