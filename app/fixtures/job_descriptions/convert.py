from pathlib import Path

import markdown


def get_markdown_for_job(job_id):
    path = Path(__file__).parent / f'job_{job_id}.md'
    content = path.read_text()
    md = markdown.markdown(content)
    return md
