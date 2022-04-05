from django.db.models import Q
from django.template.loader import render_to_string
from weasyprint import HTML

FIELD_TRANSFORMERS = {
    "clinic": "care__clinic_id",
    "department": "care__department_id",
}


def get_time_filter(**kwargs):
    time_range = kwargs["time_range"]
    year = kwargs.get("year")
    month = kwargs.get("month")
    date_from = kwargs.get("date_from")
    date_to = kwargs.get("date_to")

    q = Q()
    if time_range == "year":
        q = q & Q(updated_at__year=year)
    elif time_range == "month":
        q = q & Q(updated_at__year=year) & Q(updated_at__month=month)
    elif time_range == "custom":
        if date_from:
            q = q & Q(updated_at__gte=date_from)
        if date_to:
            q = q & Q(updated_at__lte=date_to)
    return q


def get_entity_filter(filters, field_transformers=None):
    if field_transformers is None:
        field_transformers = FIELD_TRANSFORMERS
    q = Q()
    for field, value in filters.items():
        q &= Q(**{field_transformers[field]: value})
    return q


def txt_renderer(data, **kwargs):
    template = kwargs["template"]
    content = render_to_string(template, data)
    return content


def pdf_renderer(data, **kwargs):
    template = kwargs["template"]
    content = render_to_string(template, data)
    html = HTML(string=content)
    rendered = html.write_pdf()
    return rendered
