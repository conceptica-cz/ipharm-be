from django.db.models import Q
from django.template.loader import render_to_string
from references.models import Clinic, Department

FILTER_NAMES = {
    "clinic": "Klinika",
    "department": "Oddělení",
    "atc_group_exact": "ATC skupina",
    "atc_group_startswith": "ATC skupina začíná písmeny",
    "care_type": "Typ pacienta",
}

FILTER_MODELS = {
    "clinic": Clinic,
    "department": Department,
}

FILTER_VALUES = {
    ("hospitalization",): "hospitalizované",
    ("ambulation",): "ambulantní",
    ("ambulation", "external"): "ambulantní",
    ("external", "ambulation"): "ambulantní",
    ("external",): "externí",
}


def get_func_from_path(dotted_path):
    module_name, func_name = dotted_path.rsplit(".", 1)
    module = __import__(module_name, fromlist=[func_name])
    return getattr(module, func_name)


def get_time_filter(lookup_prefix="", **kwargs):
    time_range = kwargs["time_range"]
    year = kwargs.get("year")
    month = kwargs.get("month")
    date_from = kwargs.get("date_from")
    date_to = kwargs.get("date_to")

    q = Q()
    if time_range == "year":
        q = q & Q(**{f"{lookup_prefix}updated_at__year": year})
    elif time_range == "month":
        q = (
            q
            & Q(**{f"{lookup_prefix}updated_at__year": year})
            & Q(**{f"{lookup_prefix}updated_at__month": month})
        )
    elif time_range == "custom":
        if date_from:
            q = q & Q(**{f"{lookup_prefix}updated_at__gte": date_from})
        if date_to:
            q = q & Q(**{f"{lookup_prefix}updated_at__lte": date_to})
    return q


def get_entity_filter(filters, field_lookup=None):
    q = Q()
    for field, value in filters.items():
        q &= Q(**{field_lookup[field]: value})
    return q


def get_header(**kwargs) -> str:
    time_range = kwargs["time_range"]
    if time_range == "year":
        header = f"Rok: {kwargs['year']}"
    elif time_range == "month":
        header = f"Měsíc: {kwargs['month']}/{kwargs['year']}"
    else:
        header = (
            f"Od: {kwargs.get('date_from', '...')} do: {kwargs.get('date_to', '...')}"
        )
    for f, value in kwargs.get("filters", {}).items():
        if f in FILTER_MODELS.keys():
            header += f"; {FILTER_NAMES[f]}: {FILTER_MODELS[f].objects.get(pk=value)}"
        else:
            if value in FILTER_VALUES.keys():
                value = FILTER_VALUES[value]
            header += f"; {FILTER_NAMES[f]}: {value}"
    return header


def txt_renderer(data, **kwargs):
    template = kwargs["template"]
    content = render_to_string(template, data)
    return content
