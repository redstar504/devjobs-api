import markdown


def get_html_description(job):
    md = ""
    md += f'{job["description"]}\n\n'
    md += "## Requirements\n\n"
    md += f'{job["requirements"]["content"]}\n\n'

    for item in job["requirements"]["items"]:
        md += f'- {item}'

    md += "\n\n## Role\n\n"

    md += f'{job["role"]["content"]}\n\n'

    for key, item in enumerate(job["role"]["items"]):
        md += f'{key + 1}. {item}\n'

    return markdown.markdown(md)
