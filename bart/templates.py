def project_root_template(project_name,
                          markup_language = "asciidoc"):
    match markup_language:
        case "asciidoc":
            return f"""= {project_name}"""
        case "markdown":
            return f"""# {project_name}"""
        case _:
            return ""
