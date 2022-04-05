from ipharm.models.cares import Care
from ipharm.models.checkins import CheckIn
from reports.generic_reports.common import get_entity_filter, get_time_filter


def risk_level_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    entity_filter = get_entity_filter(kwargs.get("filters", {}))

    query_set = CheckIn.objects.filter(time_filter & entity_filter)

    data = {
        "kwargs": kwargs,
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
