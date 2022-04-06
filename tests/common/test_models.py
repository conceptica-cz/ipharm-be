from django.test import TestCase
from updates.models import BaseUpdatableModel

from factories.ipharm import CheckInFactory
from factories.references import DrugFactory


class BaseUpdatableModelTest(TestCase):
    def test_get_changes(self):
        check_in = CheckInFactory(risk_level="1")

        drug_1 = DrugFactory()
        drug_2 = DrugFactory()
        drug_3 = DrugFactory()

        check_in.risk_level = "2"
        check_in.save()
        check_in.drugs.set([drug_1, drug_2])

        changes = check_in.get_changes()
        self.assertEqual(changes[0].field_changes[0].field, "drugs")

    def test_m2m_history_to_value_changes(self):
        check_in = CheckInFactory()

        drug_1 = DrugFactory()
        drug_2 = DrugFactory()
        drug_3 = DrugFactory()

        check_in.drugs.set([drug_1])
        check_in.drugs.set([drug_1, drug_2])
        check_in.drugs.set([drug_1, drug_3])

        changes = BaseUpdatableModel._m2m_history_to_value_changes(
            check_in.drugs.through.log.all(), reverse_field_name="drug"
        )
        self.assertEqual(changes[0]["old"], [])
        self.assertEqual(changes[0]["new"], [drug_1.serialize().data])
        self.assertEqual(changes[1]["old"], [drug_1.serialize().data])
        self.assertEqual(
            sorted(changes[1]["new"], key=lambda d: d["name"]),
            sorted(
                [drug_1.serialize().data, drug_2.serialize().data],
                key=lambda d: d["name"],
            ),
        )
        self.assertEqual(
            sorted(changes[2]["old"], key=lambda d: d["name"]),
            sorted(
                [drug_1.serialize().data, drug_2.serialize().data],
                key=lambda d: d["name"],
            ),
        )
        self.assertEqual(changes[2]["new"], [drug_1.serialize().data])
        self.assertEqual(changes[3]["old"], [drug_1.serialize().data])
        self.assertEqual(
            sorted(changes[3]["new"], key=lambda d: d["name"]),
            sorted(
                [drug_1.serialize().data, drug_3.serialize().data],
                key=lambda d: d["name"],
            ),
        )
        self.assertEqual(len(changes), 4)
