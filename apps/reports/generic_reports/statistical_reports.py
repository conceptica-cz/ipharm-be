from django.db.models import Count, F, Q
from ipharm.models.cares import Care
from ipharm.models.checkins import CheckIn
from ipharm.models.pharmacological_evaluations import PharmacologicalEvaluation
from references.models import Tag
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


def evaluation_patients_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    entity_filter = get_entity_filter(kwargs.get("filters", {}))

    counts = PharmacologicalEvaluation.objects.filter(
        time_filter & entity_filter
    ).aggregate(
        deployment_count=Count("care", Q(deployment=True), distinct=True),
        deployment_initial_diagnosis_count=Count(
            "care",
            Q(deployment=True) & Q(deployment_initial_diagnosis=True),
            distinct=True,
        ),
        deployment_during_diagnosis_count=Count(
            "care",
            Q(deployment=True) & Q(deployment_during_diagnosis=True),
            distinct=True,
        ),
        deployment_ft_approach_count=Count(
            "care", Q(deployment=True) & Q(deployment_ft_approach=True), distinct=True
        ),
        deployment_other_reason_count=Count(
            "care",
            Q(deployment=True) & Q(deployment_other_reason__isnull=False),
            distinct=True,
        ),
        continuation_count=Count("care", Q(continuation=True), distinct=True),
        continuation_drug_reintroduction_count=Count(
            "care",
            Q(continuation=True) & Q(continuation_drug_reintroduction=True),
            distinct=True,
        ),
        continuation_medical_intervention_count=Count(
            "care",
            Q(continuation=True) & Q(continuation_medical_intervention=True),
            distinct=True,
        ),
        continuation_other_reason_count=Count(
            "care",
            Q(continuation=True) & Q(continuation_other_reason__isnull=False),
            distinct=True,
        ),
        discontinuation_count=Count("care", Q(discontinuation=True), distinct=True),
        discontinuation_contradiction_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_contradiction=True),
            distinct=True,
        ),
        discontinuation_adverse_effect_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_adverse_effect=True),
            distinct=True,
        ),
        discontinuation_adverse_effect_risk_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_adverse_effect_risk=True),
            distinct=True,
        ),
        discontinuation_missing_indication_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_missing_indication=True),
            distinct=True,
        ),
        discontinuation_allergies_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_allergies=True),
            distinct=True,
        ),
        discontinuation_drug_interaction_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_drug_interaction=True),
            distinct=True,
        ),
        discontinuation_duplicity_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_duplicity=True),
            distinct=True,
        ),
        discontinuation_renal_insufficiency_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_renal_insufficiency=True),
            distinct=True,
        ),
        discontinuation_hepatic_insufficiency_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_hepatic_insufficiency=True),
            distinct=True,
        ),
        discontinuation_medical_intervention_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_medical_intervention=True),
            distinct=True,
        ),
        discontinuation_underdosage_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_underdosage=True),
            distinct=True,
        ),
        discontinuation_underdosage_risk_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_underdosage_risk=True),
            distinct=True,
        ),
        discontinuation_overdosage_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_overdosage=True),
            distinct=True,
        ),
        discontinuation_overdosage_risk_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_overdosage_risk=True),
            distinct=True,
        ),
        discontinuation_other_reason_count=Count(
            "care",
            Q(discontinuation=True) & Q(discontinuation_other_reason__isnull=False),
            distinct=True,
        ),
        dose_change_count=Count("care", Q(dose_change=True), distinct=True),
        dose_change_adverse_effect_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_adverse_effect=True),
            distinct=True,
        ),
        dose_change_adverse_effect_risk_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_adverse_effect_risk=True),
            distinct=True,
        ),
        dose_change_renal_insufficiency_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_renal_insufficiency=True),
            distinct=True,
        ),
        dose_change_hepatic_insufficiency_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_hepatic_insufficiency=True),
            distinct=True,
        ),
        dose_change_drug_interaction_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_drug_interaction=True),
            distinct=True,
        ),
        dose_change_underdosage_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_underdosage=True),
            distinct=True,
        ),
        dose_change_overdosage_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_overdosage=True),
            distinct=True,
        ),
        dose_change_laboratory_findings_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_laboratory_findings=True),
            distinct=True,
        ),
        dose_change_dosage_reduction_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_dosage_reduction=True),
            distinct=True,
        ),
        dose_change_dosage_increase_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_dosage_increase=True),
            distinct=True,
        ),
        dose_change_other_reason_count=Count(
            "care",
            Q(dose_change=True) & Q(dose_change_other_reason__isnull=False),
            distinct=True,
        ),
        recommended_investigation_by_specialist_count=Count(
            "care",
            Q(recommended_investigation_by_specialist=True),
            distinct=True,
        ),
        recommended_investigation_by_laboratory_count=Count(
            "care",
            Q(recommended_investigation_by_laboratory=True),
            distinct=True,
        ),
        recommended_investigation_by_physical_count=Count(
            "care",
            Q(recommended_investigation_by_physical=True),
            distinct=True,
        ),
        tdm_interpretation_count=Count(
            "care",
            Q(tdm_interpretation=True),
            distinct=True,
        ),
        tdm_measure_level_recommendation_count=Count(
            "care",
            Q(tdm_measure_level_recommendation=True),
            distinct=True,
        ),
        specific_adverse_effect_diagnosis_count=Count(
            "care",
            Q(specific_adverse_effect_diagnosis=True),
            distinct=True,
        ),
        specific_adverse_effect_reporting_count=Count(
            "care",
            Q(specific_adverse_effect_reporting=True),
            distinct=True,
        ),
        specific_consultation_count=Count(
            "care",
            Q(specific_consultation=True),
            distinct=True,
        ),
        dosage_determination_count=Count(
            "care",
            Q(dosage_determination=True),
            distinct=True,
        ),
        administration_method_optimization_count=Count(
            "care",
            Q(administration_method_optimization=True),
            distinct=True,
        ),
    )

    data = {
        "header": get_header(**kwargs),
        "counts": counts,
    }
    return data


def evaluation_patients_xlsx_data_transformer(data: dict) -> dict:
    border = {"border": 1}
    align_left = {"align": "left"}
    default = border | align_left
    bold = {"bold": True} | default
    merges = [
        (0, 0, 0, 1),
    ]
    widths = [32, 28]
    xlsx_data = [
        [
            (data["header"], default),
            ("", default),
        ],
        [
            ("", default),
            ("Počet pacientů", default),
        ],
        [
            ("Nasazení léčiva", bold),
            data["counts"]["deployment_count"],
        ],
        [
            "Diagnóza ve vstupní kontrole",
            data["counts"]["deployment_initial_diagnosis_count"],
        ],
        [
            "Diagnóza v průběhu hospitalizace",
            data["counts"]["deployment_during_diagnosis_count"],
        ],
        [
            "Vhodnější FT postup",
            data["counts"]["deployment_ft_approach_count"],
        ],
        [
            "Jiný důvod",
            data["counts"]["deployment_other_reason_count"],
        ],
        [
            ("Pokračování v terapii", bold),
            data["counts"]["continuation_count"],
        ],
        [
            "Znovunasazení léčiva",
            data["counts"]["continuation_drug_reintroduction_count"],
        ],
        [
            "Po lékařské intervenci",
            data["counts"]["continuation_medical_intervention_count"],
        ],
        [
            "Jiný důvod",
            data["counts"]["continuation_other_reason_count"],
        ],
        [
            ("Vysazení léčiva", bold),
            data["counts"]["discontinuation_count"],
        ],
        [
            "Kontraindikace",
            data["counts"]["discontinuation_contradiction_count"],
        ],
        [
            "Projev nežádoucího účinku",
            data["counts"]["discontinuation_adverse_effect_count"],
        ],
        [
            "Riziko nežádoucího účinku",
            data["counts"]["discontinuation_adverse_effect_risk_count"],
        ],
        [
            "Chybějící indikace",
            data["counts"]["discontinuation_missing_indication_count"],
        ],
        [
            "Alergie",
            data["counts"]["discontinuation_allergies_count"],
        ],
        [
            "Riziko poddávkování",
            data["counts"]["discontinuation_underdosage_risk_count"],
        ],
        [
            "Poddávkování",
            data["counts"]["discontinuation_underdosage_count"],
        ],
        [
            "Riziko předávkování",
            data["counts"]["discontinuation_overdosage_risk_count"],
        ],
        [
            "Léková interakce",
            data["counts"]["discontinuation_drug_interaction_count"],
        ],
        [
            "Duplicity",
            data["counts"]["discontinuation_duplicity_count"],
        ],
        [
            "Renální insuficience",
            data["counts"]["discontinuation_renal_insufficiency_count"],
        ],
        [
            "Hepatální insuficience",
            data["counts"]["discontinuation_hepatic_insufficiency_count"],
        ],
        [
            "Lékařská intervence",
            data["counts"]["discontinuation_medical_intervention_count"],
        ],
        [
            "Jiný důvod",
            data["counts"]["discontinuation_other_reason_count"],
        ],
        [
            "Změna dávky",
            data["counts"]["dose_change_count"],
        ],
        [
            "Projev nežádoucího účinku",
            data["counts"]["dose_change_adverse_effect_count"],
        ],
        [
            "Riziko nežádoucího účinku",
            data["counts"]["dose_change_adverse_effect_risk_count"],
        ],
        [
            "Hepatální insuficience",
            data["counts"]["dose_change_hepatic_insufficiency_count"],
        ],
        [
            "Renální insuficience",
            data["counts"]["dose_change_renal_insufficiency_count"],
        ],
        [
            "Léková interakce",
            data["counts"]["dose_change_drug_interaction_count"],
        ],
        [
            "Riziko poddávkování",
            data["counts"]["dose_change_underdosage_count"],
        ],
        [
            "Riziko předávkování",
            data["counts"]["dose_change_overdosage_count"],
        ],
        [
            "Na základě laboratorních výsledků",
            data["counts"]["dose_change_laboratory_findings_count"],
        ],
        [
            "Snížení dávky",
            data["counts"]["dose_change_dosage_reduction_count"],
        ],
        [
            "Zvýšení dávky",
            data["counts"]["dose_change_dosage_increase_count"],
        ],
        [
            "Jiný důvod",
            data["counts"]["dose_change_other_reason_count"],
        ],
        [
            ("Doporučené vyšetření", bold),
            "",
        ],
        [
            "Specialistou",
            data["counts"]["recommended_investigation_by_specialist_count"],
        ],
        [
            "Laboratoří",
            data["counts"]["recommended_investigation_by_laboratory_count"],
        ],
        [
            "Fyzikální",
            data["counts"]["recommended_investigation_by_physical_count"],
        ],
        [
            ("TDM", bold),
            "",
        ],
        [
            "Interpretace",
            data["counts"]["tdm_interpretation_count"],
        ],
        [
            "Doporučené změření hladiny",
            data["counts"]["tdm_measure_level_recommendation_count"],
        ],
        [
            ("Specifika", bold),
            "",
        ],
        [
            "Diagnostika nežádoucího účinku",
            data["counts"]["specific_adverse_effect_diagnosis_count"],
        ],
        [
            "Hlášení NÚ",
            data["counts"]["specific_adverse_effect_reporting_count"],
        ],
        [
            "Konzultace",
            data["counts"]["specific_consultation_count"],
        ],
        [
            "Stanovení dávka",
            data["counts"]["dosage_determination_count"],
        ],
        [
            "Optimalizace způsobu",
            data["counts"]["administration_method_optimization_count"],
        ],
    ]
    return {
        "data": xlsx_data,
        "widths": widths,
        "merges": merges,
        "default_format": default,
    }


def tags_loader(**kwargs) -> dict:
    evaluation_time_filter = get_time_filter(
        **kwargs, lookup_prefix="pharmacologicalevaluation__"
    )

    evaluation_filter = get_entity_filter(
        filters=kwargs.get("filters", {}),
        lookup_prefix="pharmacologicalevaluation__",
    )

    plan_time_filter = get_time_filter(**kwargs, lookup_prefix="pharmacologicalplan__")

    plan_filter = get_entity_filter(
        filters=kwargs.get("filters", {}),
        lookup_prefix="pharmacologicalplan__",
    )

    risk_drug_history_time_filter = get_time_filter(
        **kwargs, lookup_prefix="riskdrughistory__"
    )

    risk_drug_history_filter = get_entity_filter(
        filters=kwargs.get("filters", {}),
        lookup_prefix="riskdrughistory__",
    )

    tags = Tag.objects.annotate(
        evaluation_count=Count(
            "pharmacologicalevaluation",
            filter=evaluation_filter & evaluation_time_filter,
            distinct=True,
        ),
        plan_count=Count(
            "pharmacologicalplan",
            filter=plan_filter & plan_time_filter,
            distinct=True,
        ),
        history_count=Count(
            "riskdrughistory",
            filter=risk_drug_history_time_filter & risk_drug_history_filter,
            distinct=True,
        ),
        total_count=F("evaluation_count") + F("plan_count") + F("history_count"),
    ).filter(total_count__gt=0)

    data = {
        "tags": tags,
        "header": get_header(**kwargs),
    }
    return data


def tags_xlsx_data_transformer(data: dict) -> dict:
    border = {"border": 1}
    align_left = {"align": "left"}
    default = border | align_left
    merges = [
        (0, 0, 0, 1),
    ]
    widths = [28, 28]
    xlsx_data = [
        [
            (data["header"], default),
            ("", default),
        ],
        [
            ("", default),
            ("Počet pacientů", default),
        ],
    ]
    for tag in data["tags"]:
        xlsx_data.append(
            [
                (tag.name, default),
                (tag.total_count, default),
            ]
        )
    return {"data": xlsx_data, "widths": widths, "merges": merges}


def evaluation_drugs_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    entity_filter = get_entity_filter(kwargs.get("filters", {}))

    query_set = CheckIn.objects.filter(time_filter & entity_filter)

    data = {
        "header": get_header(**kwargs),
        "hospital_evaluation_drugs_1": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=1
        ).count(),
        "hospital_evaluation_drugs_2": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=2
        ).count(),
        "hospital_evaluation_drugs_3": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=3
        ).count(),
        "ambulance_evaluation_drugs_1": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=1
        ).count(),
        "ambulance_evaluation_drugs_2": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=2
        ).count(),
        "ambulance_evaluation_drugs_3": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=3
        ).count(),
    }
    return data


def evaluation_drugs_xlsx_data_transformer(data: dict) -> dict:
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
            (data["hospital_evaluation_drugs_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["hospital_evaluation_drugs_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["hospital_evaluation_drugs_3"], default),
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
            (data["ambulance_evaluation_drugs_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["ambulance_evaluation_drugs_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["ambulance_evaluation_drugs_3"], default),
            ("", default),
            ("", default),
        ],
    ]
    return {"data": xlsx_data, "widths": widths, "merges": merges}


def evaluation_atc_groups_summary_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    entity_filter = get_entity_filter(kwargs.get("filters", {}))

    query_set = CheckIn.objects.filter(time_filter & entity_filter)

    data = {
        "header": get_header(**kwargs),
        "hospital_evaluation_atc_groups_summary_1": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=1
        ).count(),
        "hospital_evaluation_atc_groups_summary_2": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=2
        ).count(),
        "hospital_evaluation_atc_groups_summary_3": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=3
        ).count(),
        "ambulance_evaluation_atc_groups_summary_1": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=1
        ).count(),
        "ambulance_evaluation_atc_groups_summary_2": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=2
        ).count(),
        "ambulance_evaluation_atc_groups_summary_3": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=3
        ).count(),
    }
    return data


def evaluation_atc_groups_summary_xlsx_data_transformer(data: dict) -> dict:
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
            (data["hospital_evaluation_atc_groups_summary_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["hospital_evaluation_atc_groups_summary_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["hospital_evaluation_atc_groups_summary_3"], default),
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
            (data["ambulance_evaluation_atc_groups_summary_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["ambulance_evaluation_atc_groups_summary_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["ambulance_evaluation_atc_groups_summary_3"], default),
            ("", default),
            ("", default),
        ],
    ]
    return {"data": xlsx_data, "widths": widths, "merges": merges}


def evaluation_atc_groups_detail_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    entity_filter = get_entity_filter(kwargs.get("filters", {}))

    query_set = CheckIn.objects.filter(time_filter & entity_filter)

    data = {
        "header": get_header(**kwargs),
        "hospital_evaluation_atc_groups_detail_1": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=1
        ).count(),
        "hospital_evaluation_atc_groups_detail_2": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=2
        ).count(),
        "hospital_evaluation_atc_groups_detail_3": query_set.filter(
            care__care_type=Care.HOSPITALIZATION, risk_level=3
        ).count(),
        "ambulance_evaluation_atc_groups_detail_1": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=1
        ).count(),
        "ambulance_evaluation_atc_groups_detail_2": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=2
        ).count(),
        "ambulance_evaluation_atc_groups_detail_3": query_set.filter(
            care__care_type=Care.AMBULATION, risk_level=3
        ).count(),
    }
    return data


def evaluation_atc_groups_detail_xlsx_data_transformer(data: dict) -> dict:
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
            (data["hospital_evaluation_atc_groups_detail_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["hospital_evaluation_atc_groups_detail_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["hospital_evaluation_atc_groups_detail_3"], default),
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
            (data["ambulance_evaluation_atc_groups_detail_1"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 2", default),
            (data["ambulance_evaluation_atc_groups_detail_2"], default),
            ("", default),
            ("", default),
        ],
        [
            ("Rizikovost 3", default),
            (data["ambulance_evaluation_atc_groups_detail_3"], default),
            ("", default),
            ("", default),
        ],
    ]
    return {"data": xlsx_data, "widths": widths, "merges": merges}
