from django.template.loader import render_to_string
from weasyprint import HTML


def pdf_renderer(data, **kwargs):
    template = kwargs["template"]
    content = render_to_string(template, data)
    html = HTML(string=content)
    rendered = html.write_pdf()
    return rendered
