def project_root_template(markup: str,
                          project_name: str):

    match markup:
        case "asciidoc":
            return f"""= {project_name}"""
        case "markdown":
            return f"""# {project_name}"""
        case _:
            return "{project_name}"
