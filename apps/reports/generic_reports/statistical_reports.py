from django.db.models import Count, F, Q, Sum
from ipharm.models.cares import Care
from ipharm.models.checkins import CheckIn
from ipharm.models.pharmacological_evaluations import PharmacologicalEvaluation
from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from references.models import Drug, Tag
from reports.generic_reports.common import (
    get_entity_filter,
    get_header,
    get_time_filter,
)


def risk_level_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    field_lookup = {
        "clinic": "care__clinic_id",
        "department": "care__department_id",
        "care_type": "care__care_type__in",
    }

    entity_filter = get_entity_filter(
        kwargs.get("filters", {}), field_lookup=field_lookup
    )

    query_set = CheckIn.objects.filter(time_filter & entity_filter)
    risk_level_counts = query_set.aggregate(
        hospital_risk_level_1=Count(
            "id",
            filter=Q(
                risk_level=1,
                care__care_type=Care.HOSPITALIZATION,
            ),
        ),
        hospital_risk_level_2=Count(
            "id",
            filter=Q(
                risk_level=2,
                care__care_type=Care.HOSPITALIZATION,
            ),
        ),
        hospital_risk_level_3=Count(
            "id",
            filter=Q(
                risk_level=3,
                care__care_type=Care.HOSPITALIZATION,
            ),
        ),
        ambulance_risk_level_1=Count(
            "id",
            filter=Q(
                risk_level=1,
                care__care_type=Care.AMBULATION,
            ),
        ),
        ambulance_risk_level_2=Count(
            "id",
            filter=Q(
                risk_level=2,
                care__care_type=Care.AMBULATION,
            ),
        ),
        ambulance_risk_level_3=Count(
            "id",
            filter=Q(
                risk_level=3,
                care__care_type=Care.AMBULATION,
            ),
        ),
    )

    query_set = PharmacologicalPlan.objects.filter(time_filter & entity_filter)
    pharmacological_plan_counts = query_set.aggregate(
        pharmacological_plan_hospital_risk_level_1=Count(
            "id",
            filter=Q(
                care__checkin__risk_level=1,
                care__care_type=Care.HOSPITALIZATION,
            ),
        ),
        pharmacological_plan_hospital_risk_level_2=Count(
            "id",
            filter=Q(
                care__checkin__risk_level=2,
                care__care_type=Care.HOSPITALIZATION,
            ),
        ),
        pharmacological_plan_hospital_risk_level_3=Count(
            "id",
            filter=Q(
                care__checkin__risk_level=3,
                care__care_type=Care.HOSPITALIZATION,
            ),
        ),
        pharmacological_plan_ambulance_risk_level_1=Count(
            "id",
            filter=Q(
                care__checkin__risk_level=1,
                care__care_type=Care.AMBULATION,
            ),
        ),
        pharmacological_plan_ambulance_risk_level_2=Count(
            "id",
            filter=Q(
                care__checkin__risk_level=2,
                care__care_type=Care.AMBULATION,
            ),
        ),
        pharmacological_plan_ambulance_risk_level_3=Count(
            "id",
            filter=Q(
                care__checkin__risk_level=3,
                care__care_type=Care.AMBULATION,
            ),
        ),
    )

    field_lookup = {
        "clinic": "pharmacological_plan__care__clinic_id",
        "department": "pharmacological_plan__care__department_id",
        "care_type": "pharmacological_plan__care__care_type",
    }

    entity_filter = get_entity_filter(
        kwargs.get("filters", {}), field_lookup=field_lookup
    )

    query_set = PharmacologicalPlanComment.objects.filter(time_filter & entity_filter)
    pharmacological_plan_verification_counts = query_set.aggregate(
        pharmacological_plan_verification_hospital_risk_level_1=Count(
            "id",
            filter=Q(
                pharmacological_plan__care__checkin__risk_level=1,
                pharmacological_plan__care__care_type=Care.HOSPITALIZATION,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ),
        ),
        pharmacological_plan_verification_hospital_risk_level_2=Count(
            "id",
            filter=Q(
                pharmacological_plan__care__checkin__risk_level=2,
                pharmacological_plan__care__care_type=Care.HOSPITALIZATION,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ),
        ),
        pharmacological_plan_verification_hospital_risk_level_3=Count(
            "id",
            filter=Q(
                pharmacological_plan__care__checkin__risk_level=3,
                pharmacological_plan__care__care_type=Care.HOSPITALIZATION,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ),
        ),
        pharmacological_plan_verification_ambulance_risk_level_1=Count(
            "id",
            filter=Q(
                pharmacological_plan__care__checkin__risk_level=1,
                pharmacological_plan__care__care_type=Care.AMBULATION,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ),
        ),
        pharmacological_plan_verification_ambulance_risk_level_2=Count(
            "id",
            filter=Q(
                pharmacological_plan__care__checkin__risk_level=2,
                pharmacological_plan__care__care_type=Care.AMBULATION,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ),
        ),
        pharmacological_plan_verification_ambulance_risk_level_3=Count(
            "id",
            filter=Q(
                pharmacological_plan__care__checkin__risk_level=3,
                pharmacological_plan__care__care_type=Care.AMBULATION,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ),
        ),
    )

    data = {
        "header": get_header(**kwargs),
        "hospital_risk_level_1": risk_level_counts["hospital_risk_level_1"],
        "hospital_risk_level_2": risk_level_counts["hospital_risk_level_2"],
        "hospital_risk_level_3": risk_level_counts["hospital_risk_level_3"],
        "ambulance_risk_level_1": risk_level_counts["ambulance_risk_level_1"],
        "ambulance_risk_level_2": risk_level_counts["ambulance_risk_level_2"],
        "ambulance_risk_level_3": risk_level_counts["ambulance_risk_level_3"],
        "pharmacological_plan_hospital_risk_level_1": pharmacological_plan_counts[
            "pharmacological_plan_hospital_risk_level_1"
        ],
        "pharmacological_plan_hospital_risk_level_2": pharmacological_plan_counts[
            "pharmacological_plan_hospital_risk_level_2"
        ],
        "pharmacological_plan_hospital_risk_level_3": pharmacological_plan_counts[
            "pharmacological_plan_hospital_risk_level_3"
        ],
        "pharmacological_plan_ambulance_risk_level_1": pharmacological_plan_counts[
            "pharmacological_plan_ambulance_risk_level_1"
        ],
        "pharmacological_plan_ambulance_risk_level_2": pharmacological_plan_counts[
            "pharmacological_plan_ambulance_risk_level_2"
        ],
        "pharmacological_plan_ambulance_risk_level_3": pharmacological_plan_counts[
            "pharmacological_plan_ambulance_risk_level_3"
        ],
        "pharmacological_plan_verification_hospital_risk_level_1": pharmacological_plan_verification_counts[
            "pharmacological_plan_verification_hospital_risk_level_1"
        ],
        "pharmacological_plan_verification_hospital_risk_level_2": pharmacological_plan_verification_counts[
            "pharmacological_plan_verification_hospital_risk_level_2"
        ],
        "pharmacological_plan_verification_hospital_risk_level_3": pharmacological_plan_verification_counts[
            "pharmacological_plan_verification_hospital_risk_level_3"
        ],
        "pharmacological_plan_verification_ambulance_risk_level_1": pharmacological_plan_verification_counts[
            "pharmacological_plan_verification_ambulance_risk_level_1"
        ],
        "pharmacological_plan_verification_ambulance_risk_level_2": pharmacological_plan_verification_counts[
            "pharmacological_plan_verification_ambulance_risk_level_2"
        ],
        "pharmacological_plan_verification_ambulance_risk_level_3": pharmacological_plan_verification_counts[
            "pharmacological_plan_verification_ambulance_risk_level_3"
        ],
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
            ("Hospitalizovan?? pacienti", default),
            ("", default),
            ("", default),
        ],
        [
            ("", default),
            ("Po??et pacient??", default),
            ("Po??et stanoven??ch FK pl??n??", default),
            ("Po??et ov????en??ch FK pl??n??", default),
        ],
        [
            ("Rizikovost 1", default),
            (data["hospital_risk_level_1"], default),
            (data["pharmacological_plan_hospital_risk_level_1"], default),
            (data["pharmacological_plan_verification_hospital_risk_level_1"], default),
        ],
        [
            ("Rizikovost 2", default),
            (data["hospital_risk_level_2"], default),
            (data["pharmacological_plan_hospital_risk_level_2"], default),
            (data["pharmacological_plan_verification_hospital_risk_level_2"], default),
        ],
        [
            ("Rizikovost 3", default),
            (data["hospital_risk_level_3"], default),
            (data["pharmacological_plan_hospital_risk_level_3"], default),
            (data["pharmacological_plan_verification_hospital_risk_level_3"], default),
        ],
        [
            ("", default),
            ("Ambulantn?? pacienti", default),
            ("", default),
            ("", default),
        ],
        [
            ("", default),
            ("Po??et pacient??", default),
            ("Po??et stanoven??ch FK pl??n??", default),
            ("Po??et ov????en??ch FK pl??n??", default),
        ],
        [
            ("Rizikovost 1", default),
            (data["ambulance_risk_level_1"], default),
            (data["pharmacological_plan_ambulance_risk_level_1"], default),
            (data["pharmacological_plan_verification_ambulance_risk_level_1"], default),
        ],
        [
            ("Rizikovost 2", default),
            (data["ambulance_risk_level_2"], default),
            (data["pharmacological_plan_ambulance_risk_level_2"], default),
            (data["pharmacological_plan_verification_ambulance_risk_level_2"], default),
        ],
        [
            ("Rizikovost 3", default),
            (data["ambulance_risk_level_3"], default),
            (data["pharmacological_plan_ambulance_risk_level_3"], default),
            (data["pharmacological_plan_verification_ambulance_risk_level_3"], default),
        ],
    ]
    return {"data": xlsx_data, "widths": widths, "merges": merges}


def evaluation_patients_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs)

    field_lookup = {
        "clinic": "care__clinic_id",
        "department": "care__department_id",
        "care_type": "care__care_type__in",
    }

    entity_filter = get_entity_filter(
        kwargs.get("filters", {}), field_lookup=field_lookup
    )

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
            ("Po??et pacient??", default),
        ],
        [
            ("Nasazen?? l????iva", bold),
            data["counts"]["deployment_count"],
        ],
        [
            "Diagn??za ve vstupn?? kontrole",
            data["counts"]["deployment_initial_diagnosis_count"],
        ],
        [
            "Diagn??za v pr??b??hu hospitalizace",
            data["counts"]["deployment_during_diagnosis_count"],
        ],
        [
            "Vhodn??j???? FT postup",
            data["counts"]["deployment_ft_approach_count"],
        ],
        [
            "Jin?? d??vod",
            data["counts"]["deployment_other_reason_count"],
        ],
        [
            ("Pokra??ov??n?? v terapii", bold),
            data["counts"]["continuation_count"],
        ],
        [
            "Znovunasazen?? l????iva",
            data["counts"]["continuation_drug_reintroduction_count"],
        ],
        [
            "Po l??ka??sk?? intervenci",
            data["counts"]["continuation_medical_intervention_count"],
        ],
        [
            "Jin?? d??vod",
            data["counts"]["continuation_other_reason_count"],
        ],
        [
            ("Vysazen?? l????iva", bold),
            data["counts"]["discontinuation_count"],
        ],
        [
            "Kontraindikace",
            data["counts"]["discontinuation_contradiction_count"],
        ],
        [
            "Projev ne????douc??ho ????inku",
            data["counts"]["discontinuation_adverse_effect_count"],
        ],
        [
            "Riziko ne????douc??ho ????inku",
            data["counts"]["discontinuation_adverse_effect_risk_count"],
        ],
        [
            "Chyb??j??c?? indikace",
            data["counts"]["discontinuation_missing_indication_count"],
        ],
        [
            "Alergie",
            data["counts"]["discontinuation_allergies_count"],
        ],
        [
            "Riziko podd??vkov??n??",
            data["counts"]["discontinuation_underdosage_risk_count"],
        ],
        [
            "Podd??vkov??n??",
            data["counts"]["discontinuation_underdosage_count"],
        ],
        [
            "Riziko p??ed??vkov??n??",
            data["counts"]["discontinuation_overdosage_risk_count"],
        ],
        [
            "L??kov?? interakce",
            data["counts"]["discontinuation_drug_interaction_count"],
        ],
        [
            "Duplicity",
            data["counts"]["discontinuation_duplicity_count"],
        ],
        [
            "Ren??ln?? insuficience",
            data["counts"]["discontinuation_renal_insufficiency_count"],
        ],
        [
            "Hepat??ln?? insuficience",
            data["counts"]["discontinuation_hepatic_insufficiency_count"],
        ],
        [
            "L??ka??sk?? intervence",
            data["counts"]["discontinuation_medical_intervention_count"],
        ],
        [
            "Jin?? d??vod",
            data["counts"]["discontinuation_other_reason_count"],
        ],
        [
            ("Zm??na d??vky", bold),
            data["counts"]["dose_change_count"],
        ],
        [
            "Projev ne????douc??ho ????inku",
            data["counts"]["dose_change_adverse_effect_count"],
        ],
        [
            "Riziko ne????douc??ho ????inku",
            data["counts"]["dose_change_adverse_effect_risk_count"],
        ],
        [
            "Hepat??ln?? insuficience",
            data["counts"]["dose_change_hepatic_insufficiency_count"],
        ],
        [
            "Ren??ln?? insuficience",
            data["counts"]["dose_change_renal_insufficiency_count"],
        ],
        [
            "L??kov?? interakce",
            data["counts"]["dose_change_drug_interaction_count"],
        ],
        [
            "Riziko podd??vkov??n??",
            data["counts"]["dose_change_underdosage_count"],
        ],
        [
            "Riziko p??ed??vkov??n??",
            data["counts"]["dose_change_overdosage_count"],
        ],
        [
            "Na z??klad?? laboratorn??ch v??sledk??",
            data["counts"]["dose_change_laboratory_findings_count"],
        ],
        [
            "Sn????en?? d??vky",
            data["counts"]["dose_change_dosage_reduction_count"],
        ],
        [
            "Zv????en?? d??vky",
            data["counts"]["dose_change_dosage_increase_count"],
        ],
        [
            "Jin?? d??vod",
            data["counts"]["dose_change_other_reason_count"],
        ],
        [
            ("Doporu??en?? vy??et??en??", bold),
            "",
        ],
        [
            "Specialistou",
            data["counts"]["recommended_investigation_by_specialist_count"],
        ],
        [
            "Laborato????",
            data["counts"]["recommended_investigation_by_laboratory_count"],
        ],
        [
            "Fyzik??ln??",
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
            "Doporu??en?? zm????en?? hladiny",
            data["counts"]["tdm_measure_level_recommendation_count"],
        ],
        [
            ("Specifika", bold),
            "",
        ],
        [
            "Diagnostika ne????douc??ho ????inku",
            data["counts"]["specific_adverse_effect_diagnosis_count"],
        ],
        [
            "Hl????en?? N??",
            data["counts"]["specific_adverse_effect_reporting_count"],
        ],
        [
            "Konzultace",
            data["counts"]["specific_consultation_count"],
        ],
        [
            "Stanoven?? d??vka",
            data["counts"]["dosage_determination_count"],
        ],
        [
            "Optimalizace zp??sobu",
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

    field_lookup = {
        "clinic": "pharmacologicalevaluation__care__clinic_id",
        "department": "pharmacologicalevaluation__care__department_id",
        "care_type": "pharmacologicalevaluation__care__care_type",
    }
    evaluation_filter = get_entity_filter(
        filters=kwargs.get("filters", {}),
        field_lookup=field_lookup,
    )

    plan_time_filter = get_time_filter(**kwargs, lookup_prefix="pharmacologicalplan__")

    field_lookup = {
        "clinic": "pharmacologicalplan__care__clinic_id",
        "department": "pharmacologicalplan__care__department_id",
        "care_type": "pharmacologicalplan__care__care_type",
    }
    plan_filter = get_entity_filter(
        filters=kwargs.get("filters", {}),
        field_lookup=field_lookup,
    )

    risk_drug_history_time_filter = get_time_filter(
        **kwargs, lookup_prefix="riskdrughistory__"
    )

    field_lookup = {
        "clinic": "riskdrughistory__care__clinic_id",
        "department": "riskdrughistory__care__department_id",
        "care_type": "riskdrughistory__care__care_type",
    }
    risk_drug_history_filter = get_entity_filter(
        filters=kwargs.get("filters", {}),
        field_lookup=field_lookup,
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
            ("Po??et pacient??", default),
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
    time_filter = get_time_filter(**kwargs, lookup_prefix="pharmacologicalevaluation__")

    field_lookup = {
        "clinic": "pharmacologicalevaluation__care__clinic_id",
        "department": "pharmacologicalevaluation__care__department_id",
        "atc_group_exact": "atc_group__exact",
    }

    entity_filter = get_entity_filter(
        filters=kwargs.get("filters", {}), field_lookup=field_lookup
    )

    drugs = (
        Drug.objects.annotate(
            deployment_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_initial_diagnosis_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_initial_diagnosis=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_during_diagnosis_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_during_diagnosis=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_ft_approach_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_ft_approach=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_other_reason__isnull=False)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_drug_reintroduction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & Q(pharmacologicalevaluation__continuation_drug_reintroduction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_medical_intervention_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & Q(pharmacologicalevaluation__continuation_medical_intervention=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & Q(pharmacologicalevaluation__continuation_other_reason__isnull=False)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_contradiction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_contradiction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_adverse_effect_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_adverse_effect=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_adverse_effect_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_adverse_effect_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_missing_indication_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_missing_indication=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_allergies_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_allergies=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_drug_interaction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_drug_interaction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_duplicity_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_duplicity=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_renal_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_renal_insufficiency=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_hepatic_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(
                    pharmacologicalevaluation__discontinuation_hepatic_insufficiency=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_medical_intervention_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(
                    pharmacologicalevaluation__discontinuation_medical_intervention=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_underdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_underdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_underdosage_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_underdosage_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_overdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_overdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_overdosage_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_overdosage_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(
                    pharmacologicalevaluation__discontinuation_other_reason__isnull=False
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_adverse_effect_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_adverse_effect=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_adverse_effect_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_adverse_effect_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_renal_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_renal_insufficiency=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_hepatic_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_hepatic_insufficiency=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_drug_interaction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_drug_interaction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_underdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_underdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_overdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_overdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_laboratory_findings_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_laboratory_findings=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_dosage_reduction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_dosage_reduction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_dosage_increase_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_dosage_increase=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_other_reason__isnull=False)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            recommended_investigation_by_specialist_count=Count(
                "pharmacologicalevaluation",
                Q(
                    pharmacologicalevaluation__recommended_investigation_by_specialist=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            recommended_investigation_by_laboratory_count=Count(
                "pharmacologicalevaluation",
                Q(
                    pharmacologicalevaluation__recommended_investigation_by_laboratory=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            recommended_investigation_by_physical_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__recommended_investigation_by_physical=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            tdm_interpretation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__tdm_interpretation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            tdm_measure_level_recommendation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__tdm_measure_level_recommendation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            specific_adverse_effect_diagnosis_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__specific_adverse_effect_diagnosis=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            specific_adverse_effect_reporting_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__specific_adverse_effect_reporting=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            specific_consultation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__specific_consultation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dosage_determination_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dosage_determination=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            administration_method_optimization_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__administration_method_optimization=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
        )
        .filter(
            Q(deployment_count__gt=0)
            | Q(continuation_count__gt=0)
            | Q(discontinuation_count__gt=0)
            | Q(dose_change_count__gt=0)
            | Q(recommended_investigation_by_specialist_count__gt=0)
            | Q(recommended_investigation_by_laboratory_count__gt=0)
            | Q(recommended_investigation_by_physical_count__gt=0)
            | Q(tdm_interpretation_count__gt=0)
            | Q(tdm_measure_level_recommendation_count__gt=0)
            | Q(specific_adverse_effect_diagnosis_count__gt=0)
            | Q(specific_adverse_effect_reporting_count__gt=0)
            | Q(specific_consultation_count__gt=0)
            | Q(dosage_determination_count__gt=0)
            | Q(administration_method_optimization_count__gt=0)
        )
        .order_by("name")
    )

    counts = {}

    for drug in drugs.values():
        for counter, value in drug.items():
            if "_count" in counter:
                counts.setdefault(counter, {})[drug["name"]] = value

    data = {
        "header": get_header(**kwargs),
        "drugs": drugs,
        "counts": counts,
        "columns": drugs.count() + 1,
    }
    return data


def _evaluation_drugs_counters(data, counter_name):
    counters = []
    for drug in data["drugs"]:
        counters.append(data["counts"][counter_name][drug.name])
    return counters


def evaluation_drugs_xlsx_data_transformer(data: dict) -> dict:
    border = {"border": 1}
    align_left = {"align": "left"}
    default = border | align_left
    bold = {"bold": True} | default
    merges = [
        (0, 0, 0, data["columns"] - 1),
    ]
    widths = [32] * data["columns"]
    xlsx_data = [
        [
            (data["header"], default),
        ]
        + [""] * (data["columns"] - 1),
        [""] + [drug.name for drug in data["drugs"]],
        [
            ("Nasazen?? l????iva", bold),
        ]
        + _evaluation_drugs_counters(data, "deployment_count"),
        [
            "Diagn??za ve vstupn?? kontrole",
        ]
        + _evaluation_drugs_counters(data, "deployment_initial_diagnosis_count"),
        [
            "Diagn??za v pr??b??hu hospitalizace",
        ]
        + _evaluation_drugs_counters(data, "deployment_during_diagnosis_count"),
        [
            "Vhodn??j???? FT postup",
        ]
        + _evaluation_drugs_counters(data, "deployment_ft_approach_count"),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_drugs_counters(data, "deployment_other_reason_count"),
        [
            ("Pokra??ov??n?? v terapii", bold),
        ]
        + _evaluation_drugs_counters(data, "continuation_count"),
        [
            "Znovunasazen?? l????iva",
        ]
        + _evaluation_drugs_counters(data, "continuation_drug_reintroduction_count"),
        [
            "Po l??ka??sk?? intervenci",
        ]
        + _evaluation_drugs_counters(data, "continuation_medical_intervention_count"),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_drugs_counters(data, "continuation_other_reason_count"),
        [
            ("Vysazen?? l????iva", bold),
        ]
        + _evaluation_drugs_counters(data, "discontinuation_count"),
        [
            "Kontraindikace",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_contradiction_count"),
        [
            "Projev ne????douc??ho ????inku",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_adverse_effect_count"),
        [
            "Riziko ne????douc??ho ????inku",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_adverse_effect_risk_count"),
        [
            "Chyb??j??c?? indikace",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_missing_indication_count"),
        [
            "Alergie",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_allergies_count"),
        [
            "Riziko podd??vkov??n??",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_underdosage_risk_count"),
        [
            "Podd??vkov??n??",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_underdosage_count"),
        [
            "Riziko p??ed??vkov??n??",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_overdosage_risk_count"),
        [
            "L??kov?? interakce",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_drug_interaction_count"),
        [
            "Duplicity",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_duplicity_count"),
        [
            "Ren??ln?? insuficience",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_renal_insufficiency_count"),
        [
            "Hepat??ln?? insuficience",
        ]
        + _evaluation_drugs_counters(
            data, "discontinuation_hepatic_insufficiency_count"
        ),
        [
            "L??ka??sk?? intervence",
        ]
        + _evaluation_drugs_counters(
            data, "discontinuation_medical_intervention_count"
        ),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_drugs_counters(data, "discontinuation_other_reason_count"),
        [
            ("Zm??na d??vky", bold),
        ]
        + _evaluation_drugs_counters(data, "dose_change_count"),
        [
            "Projev ne????douc??ho ????inku",
        ]
        + _evaluation_drugs_counters(data, "dose_change_adverse_effect_count"),
        [
            "Riziko ne????douc??ho ????inku",
        ]
        + _evaluation_drugs_counters(data, "dose_change_adverse_effect_risk_count"),
        [
            "Hepat??ln?? insuficience",
        ]
        + _evaluation_drugs_counters(data, "dose_change_hepatic_insufficiency_count"),
        [
            "Ren??ln?? insuficience",
        ]
        + _evaluation_drugs_counters(data, "dose_change_renal_insufficiency_count"),
        [
            "L??kov?? interakce",
        ]
        + _evaluation_drugs_counters(data, "dose_change_drug_interaction_count"),
        [
            "Riziko podd??vkov??n??",
        ]
        + _evaluation_drugs_counters(data, "dose_change_underdosage_count"),
        [
            "Riziko p??ed??vkov??n??",
        ]
        + _evaluation_drugs_counters(data, "dose_change_overdosage_count"),
        [
            "Na z??klad?? laboratorn??ch v??sledk??",
        ]
        + _evaluation_drugs_counters(data, "dose_change_laboratory_findings_count"),
        [
            "Sn????en?? d??vky",
        ]
        + _evaluation_drugs_counters(data, "dose_change_dosage_reduction_count"),
        [
            "Zv????en?? d??vky",
        ]
        + _evaluation_drugs_counters(data, "dose_change_dosage_increase_count"),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_drugs_counters(data, "dose_change_other_reason_count"),
        [
            ("Doporu??en?? vy??et??en??", bold),
            "",
        ]
        + [""] * (data["columns"] - 2),
        [
            "Specialistou",
        ]
        + _evaluation_drugs_counters(
            data, "recommended_investigation_by_specialist_count"
        ),
        [
            "Laborato????",
        ]
        + _evaluation_drugs_counters(
            data, "recommended_investigation_by_laboratory_count"
        ),
        [
            "Fyzik??ln??",
        ]
        + _evaluation_drugs_counters(
            data, "recommended_investigation_by_physical_count"
        ),
        [
            ("TDM", bold),
            "",
        ]
        + [""] * (data["columns"] - 2),
        [
            "Interpretace",
        ]
        + _evaluation_drugs_counters(data, "tdm_interpretation_count"),
        [
            "Doporu??en?? zm????en?? hladiny",
        ]
        + _evaluation_drugs_counters(data, "tdm_measure_level_recommendation_count"),
        [
            ("Specifika", bold),
            "",
        ]
        + [""] * (data["columns"] - 2),
        [
            "Diagnostika ne????douc??ho ????inku",
        ]
        + _evaluation_drugs_counters(data, "specific_adverse_effect_diagnosis_count"),
        [
            "Hl????en?? N??",
        ]
        + _evaluation_drugs_counters(data, "specific_adverse_effect_reporting_count"),
        [
            "Konzultace",
        ]
        + _evaluation_drugs_counters(data, "specific_consultation_count"),
        [
            "Stanoven?? d??vka",
        ]
        + _evaluation_drugs_counters(data, "dosage_determination_count"),
        [
            "Optimalizace zp??sobu",
        ]
        + _evaluation_drugs_counters(data, "administration_method_optimization_count"),
    ]
    return {
        "data": xlsx_data,
        "widths": widths,
        "merges": merges,
        "default_format": default,
    }


def evaluation_groups_loader(**kwargs) -> dict:
    time_filter = get_time_filter(**kwargs, lookup_prefix="pharmacologicalevaluation__")

    field_lookup = {
        "clinic": "pharmacologicalevaluation__care__clinic_id",
        "department": "pharmacologicalevaluation__care__department_id",
        "atc_group_startswith": "atc_group__startswith",
    }

    entity_filter = get_entity_filter(
        filters=kwargs.get("filters", {}), field_lookup=field_lookup
    )

    groups = (
        Drug.objects.values("atc_group")
        .annotate(
            deployment_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_initial_diagnosis_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_initial_diagnosis=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_during_diagnosis_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_during_diagnosis=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_ft_approach_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_ft_approach=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            deployment_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__deployment=True)
                & Q(pharmacologicalevaluation__deployment_other_reason__isnull=False)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_drug_reintroduction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & Q(pharmacologicalevaluation__continuation_drug_reintroduction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_medical_intervention_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & Q(pharmacologicalevaluation__continuation_medical_intervention=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            continuation_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__continuation=True)
                & Q(pharmacologicalevaluation__continuation_other_reason__isnull=False)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_contradiction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_contradiction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_adverse_effect_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_adverse_effect=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_adverse_effect_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_adverse_effect_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_missing_indication_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_missing_indication=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_allergies_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_allergies=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_drug_interaction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_drug_interaction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_duplicity_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_duplicity=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_renal_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_renal_insufficiency=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_hepatic_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(
                    pharmacologicalevaluation__discontinuation_hepatic_insufficiency=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_medical_intervention_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(
                    pharmacologicalevaluation__discontinuation_medical_intervention=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_underdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_underdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_underdosage_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_underdosage_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_overdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_overdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_overdosage_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(pharmacologicalevaluation__discontinuation_overdosage_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            discontinuation_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__discontinuation=True)
                & Q(
                    pharmacologicalevaluation__discontinuation_other_reason__isnull=False
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_adverse_effect_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_adverse_effect=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_adverse_effect_risk_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_adverse_effect_risk=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_renal_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_renal_insufficiency=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_hepatic_insufficiency_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_hepatic_insufficiency=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_drug_interaction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_drug_interaction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_underdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_underdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_overdosage_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_overdosage=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_laboratory_findings_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_laboratory_findings=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_dosage_reduction_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_dosage_reduction=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_dosage_increase_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_dosage_increase=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dose_change_other_reason_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dose_change=True)
                & Q(pharmacologicalevaluation__dose_change_other_reason__isnull=False)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            recommended_investigation_by_specialist_count=Count(
                "pharmacologicalevaluation",
                Q(
                    pharmacologicalevaluation__recommended_investigation_by_specialist=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            recommended_investigation_by_laboratory_count=Count(
                "pharmacologicalevaluation",
                Q(
                    pharmacologicalevaluation__recommended_investigation_by_laboratory=True
                )
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            recommended_investigation_by_physical_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__recommended_investigation_by_physical=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            tdm_interpretation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__tdm_interpretation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            tdm_measure_level_recommendation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__tdm_measure_level_recommendation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            specific_adverse_effect_diagnosis_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__specific_adverse_effect_diagnosis=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            specific_adverse_effect_reporting_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__specific_adverse_effect_reporting=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            specific_consultation_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__specific_consultation=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            dosage_determination_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__dosage_determination=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
            administration_method_optimization_count=Count(
                "pharmacologicalevaluation",
                Q(pharmacologicalevaluation__administration_method_optimization=True)
                & entity_filter
                & time_filter,
                distinct=True,
            ),
        )
        .filter(
            Q(deployment_count__gt=0)
            | Q(continuation_count__gt=0)
            | Q(discontinuation_count__gt=0)
            | Q(dose_change_count__gt=0)
            | Q(recommended_investigation_by_specialist_count__gt=0)
            | Q(recommended_investigation_by_laboratory_count__gt=0)
            | Q(recommended_investigation_by_physical_count__gt=0)
            | Q(tdm_interpretation_count__gt=0)
            | Q(tdm_measure_level_recommendation_count__gt=0)
            | Q(specific_adverse_effect_diagnosis_count__gt=0)
            | Q(specific_adverse_effect_reporting_count__gt=0)
            | Q(specific_consultation_count__gt=0)
            | Q(dosage_determination_count__gt=0)
            | Q(administration_method_optimization_count__gt=0)
        )
        .order_by("atc_group")
    )

    counts = {}

    for group in groups:
        for counter, value in group.items():
            if "_count" in counter:
                counts.setdefault(counter, {})[group["atc_group"]] = value

    data = {
        "header": get_header(**kwargs),
        "groups": groups,
        "counts": counts,
        "columns": groups.count() + 1,
    }
    return data


def _evaluation_groups_counters(data, counter_name):
    counters = []
    for group in data["groups"]:
        counters.append(data["counts"][counter_name][group["atc_group"]])
    return counters


def evaluation_groups_xlsx_data_transformer(data: dict) -> dict:
    border = {"border": 1}
    align_left = {"align": "left"}
    default = border | align_left
    bold = {"bold": True} | default
    merges = [
        (0, 0, 0, data["columns"] - 1),
    ]
    widths = [32] * data["columns"]
    xlsx_data = [
        [
            (data["header"], default),
        ]
        + [""] * (data["columns"] - 1),
        [""] + [group["atc_group"] for group in data["groups"]],
        [
            ("Nasazen?? l????iva", bold),
        ]
        + _evaluation_groups_counters(data, "deployment_count"),
        [
            "Diagn??za ve vstupn?? kontrole",
        ]
        + _evaluation_groups_counters(data, "deployment_initial_diagnosis_count"),
        [
            "Diagn??za v pr??b??hu hospitalizace",
        ]
        + _evaluation_groups_counters(data, "deployment_during_diagnosis_count"),
        [
            "Vhodn??j???? FT postup",
        ]
        + _evaluation_groups_counters(data, "deployment_ft_approach_count"),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_groups_counters(data, "deployment_other_reason_count"),
        [
            ("Pokra??ov??n?? v terapii", bold),
        ]
        + _evaluation_groups_counters(data, "continuation_count"),
        [
            "Znovunasazen?? l????iva",
        ]
        + _evaluation_groups_counters(data, "continuation_drug_reintroduction_count"),
        [
            "Po l??ka??sk?? intervenci",
        ]
        + _evaluation_groups_counters(data, "continuation_medical_intervention_count"),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_groups_counters(data, "continuation_other_reason_count"),
        [
            ("Vysazen?? l????iva", bold),
        ]
        + _evaluation_groups_counters(data, "discontinuation_count"),
        [
            "Kontraindikace",
        ]
        + _evaluation_groups_counters(data, "discontinuation_contradiction_count"),
        [
            "Projev ne????douc??ho ????inku",
        ]
        + _evaluation_groups_counters(data, "discontinuation_adverse_effect_count"),
        [
            "Riziko ne????douc??ho ????inku",
        ]
        + _evaluation_groups_counters(
            data, "discontinuation_adverse_effect_risk_count"
        ),
        [
            "Chyb??j??c?? indikace",
        ]
        + _evaluation_groups_counters(data, "discontinuation_missing_indication_count"),
        [
            "Alergie",
        ]
        + _evaluation_groups_counters(data, "discontinuation_allergies_count"),
        [
            "Riziko podd??vkov??n??",
        ]
        + _evaluation_groups_counters(data, "discontinuation_underdosage_risk_count"),
        [
            "Podd??vkov??n??",
        ]
        + _evaluation_groups_counters(data, "discontinuation_underdosage_count"),
        [
            "Riziko p??ed??vkov??n??",
        ]
        + _evaluation_groups_counters(data, "discontinuation_overdosage_risk_count"),
        [
            "L??kov?? interakce",
        ]
        + _evaluation_groups_counters(data, "discontinuation_drug_interaction_count"),
        [
            "Duplicity",
        ]
        + _evaluation_groups_counters(data, "discontinuation_duplicity_count"),
        [
            "Ren??ln?? insuficience",
        ]
        + _evaluation_groups_counters(
            data, "discontinuation_renal_insufficiency_count"
        ),
        [
            "Hepat??ln?? insuficience",
        ]
        + _evaluation_groups_counters(
            data, "discontinuation_hepatic_insufficiency_count"
        ),
        [
            "L??ka??sk?? intervence",
        ]
        + _evaluation_groups_counters(
            data, "discontinuation_medical_intervention_count"
        ),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_groups_counters(data, "discontinuation_other_reason_count"),
        [
            ("Zm??na d??vky", bold),
        ]
        + _evaluation_groups_counters(data, "dose_change_count"),
        [
            "Projev ne????douc??ho ????inku",
        ]
        + _evaluation_groups_counters(data, "dose_change_adverse_effect_count"),
        [
            "Riziko ne????douc??ho ????inku",
        ]
        + _evaluation_groups_counters(data, "dose_change_adverse_effect_risk_count"),
        [
            "Hepat??ln?? insuficience",
        ]
        + _evaluation_groups_counters(data, "dose_change_hepatic_insufficiency_count"),
        [
            "Ren??ln?? insuficience",
        ]
        + _evaluation_groups_counters(data, "dose_change_renal_insufficiency_count"),
        [
            "L??kov?? interakce",
        ]
        + _evaluation_groups_counters(data, "dose_change_drug_interaction_count"),
        [
            "Riziko podd??vkov??n??",
        ]
        + _evaluation_groups_counters(data, "dose_change_underdosage_count"),
        [
            "Riziko p??ed??vkov??n??",
        ]
        + _evaluation_groups_counters(data, "dose_change_overdosage_count"),
        [
            "Na z??klad?? laboratorn??ch v??sledk??",
        ]
        + _evaluation_groups_counters(data, "dose_change_laboratory_findings_count"),
        [
            "Sn????en?? d??vky",
        ]
        + _evaluation_groups_counters(data, "dose_change_dosage_reduction_count"),
        [
            "Zv????en?? d??vky",
        ]
        + _evaluation_groups_counters(data, "dose_change_dosage_increase_count"),
        [
            "Jin?? d??vod",
        ]
        + _evaluation_groups_counters(data, "dose_change_other_reason_count"),
        [
            ("Doporu??en?? vy??et??en??", bold),
            "",
        ]
        + [""] * (data["columns"] - 2),
        [
            "Specialistou",
        ]
        + _evaluation_groups_counters(
            data, "recommended_investigation_by_specialist_count"
        ),
        [
            "Laborato????",
        ]
        + _evaluation_groups_counters(
            data, "recommended_investigation_by_laboratory_count"
        ),
        [
            "Fyzik??ln??",
        ]
        + _evaluation_groups_counters(
            data, "recommended_investigation_by_physical_count"
        ),
        [
            ("TDM", bold),
            "",
        ]
        + [""] * (data["columns"] - 2),
        [
            "Interpretace",
        ]
        + _evaluation_groups_counters(data, "tdm_interpretation_count"),
        [
            "Doporu??en?? zm????en?? hladiny",
        ]
        + _evaluation_groups_counters(data, "tdm_measure_level_recommendation_count"),
        [
            ("Specifika", bold),
            "",
        ]
        + [""] * (data["columns"] - 2),
        [
            "Diagnostika ne????douc??ho ????inku",
        ]
        + _evaluation_groups_counters(data, "specific_adverse_effect_diagnosis_count"),
        [
            "Hl????en?? N??",
        ]
        + _evaluation_groups_counters(data, "specific_adverse_effect_reporting_count"),
        [
            "Konzultace",
        ]
        + _evaluation_groups_counters(data, "specific_consultation_count"),
        [
            "Stanoven?? d??vka",
        ]
        + _evaluation_groups_counters(data, "dosage_determination_count"),
        [
            "Optimalizace zp??sobu",
        ]
        + _evaluation_groups_counters(data, "administration_method_optimization_count"),
    ]
    return {
        "data": xlsx_data,
        "widths": widths,
        "merges": merges,
        "default_format": default,
    }
