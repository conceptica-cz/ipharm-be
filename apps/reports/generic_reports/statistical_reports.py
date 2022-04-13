from ipharm.models.cares import Care
from ipharm.models.checkins import CheckIn
from reports.generic_reports.common import (
    get_entity_filter,
    get_header,
    get_time_filter,
)


def risk_level_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    entity_filter = get_entity_filter(kwargs.get("filters", {}))

    query_set = CheckIn.objects.filter(time_filter & entity_filter)

    data = {
        "header": get_header(**kwargs),
        "hospital_risk_level_1": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=1
        ).count(),
        "hospital_risk_level_2": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=2
        ).count(),
        "hospital_risk_level_3": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=3
        ).count(),
        "ambulance_risk_level_1": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=1
        ).count(),
        "ambulance_risk_level_2": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=2
        ).count(),
        "ambulance_risk_level_3": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=3
        ).count(),
    }
    return data


def risk_level_xlsx_data_transformer(data: dict) -> dict:
    border = {"border": 1}
    align_left = {"align": "left"}
    default = border | align_left
    merges = [
        (0, 0, 0, 3),
        (1, 1, 1, 3),
        (6, 1, 6, 3),
    ]
    widths = [14, 14, 28, 24]
    xlsx_data = [
        [
            (data["header"], default),
            ("", default),
            ("", default),
            ("", default),
        ],
        [
            ("", default),
            ("Hospitalizovaní pacienti", default),
            ("", default),
            ("", default),
        ],
        [
            ("", default),
            ("Počet pacientů", default),
            ("Počet stanovených FK plánů", default),
            ("Počet ověřených FK plánů", default),
        ],
        [
            ("Rizikovost 1", default),
            (data["hospital_risk_level_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["hospital_risk_level_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["hospital_risk_level_3"], default),
            ("", default),
            ("", default),
        ],
        [
            ("", default),
            ("Ambulantní pacienti", default),
            ("", default),
            ("", default),
        ],
        [
            ("", default),
            ("Počet pacientů", default),
            ("Počet stanovených FK plánů", default),
            ("Počet ověřených FK plánů", default),
        ],
        [
            ("Rizikovost 1", default),
            (data["ambulance_risk_level_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["ambulance_risk_level_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["ambulance_risk_level_3"], default),
            ("", default),
            ("", default),
        ],
    ]
    return {"data": xlsx_data, "widths": widths, "merges": merges}
