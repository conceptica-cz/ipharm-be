from django.test import TestCase, override_settings
from django.utils import timezone
from updates.models import BaseUpdatableModel, FieldChange, ModelChange

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

    @override_settings(CHANGE_HISTORY_MAX_INTERVAL=500)
    def test_merge_changes(self):
        changes = [
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 0),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field1", old="value1_1", new="value1_2"),
                    FieldChange(field="field2", old="value2_1", new="value2_2"),
                ],
            ),
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 1),
                user="user2",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field3", old="value3_1_u2", new="value3_2_u2"),
                ],
            ),
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 2),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field3", old="value3_1", new="value3_2"),
                ],
            ),
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 3),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field3", old="value3_2", new="value3_3"),
                ],
            ),
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 1, 0),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field1", old="value1_2", new="value1_3"),
                    FieldChange(field="field2", old="value2_2", new="value2_3"),
                ],
            ),
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 1, 2),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field3", old="value3_3", new="value3_4"),
                ],
            ),
        ]

        merged_changes = BaseUpdatableModel._merge_changes(
            sorted(changes, key=lambda x: x.date, reverse=True)
        )

        self.assertEqual(
            merged_changes[2],
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 0),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field1", old="value1_1", new="value1_2"),
                    FieldChange(field="field2", old="value2_1", new="value2_2"),
                    FieldChange(field="field3", old="value3_1", new="value3_3"),
                ],
            ),
        )

        self.assertEqual(
            merged_changes[1],
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 1),
                user="user2",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field3", old="value3_1_u2", new="value3_2_u2"),
                ],
            ),
        )

        self.assertEqual(
            merged_changes[0],
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 1, 0),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field1", old="value1_2", new="value1_3"),
                    FieldChange(field="field2", old="value2_2", new="value2_3"),
                    FieldChange(field="field3", old="value3_3", new="value3_4"),
                ],
            ),
        )

        self.assertEqual(len(merged_changes), 3)


class TestModelChange(TestCase):
    def test_add_changes(self):
        change_1 = ModelChange(
            date=timezone.datetime(2020, 1, 1, 0, 0, 0, 0),
            user="user1",
            entity_name="entity1",
            entity_id=1,
            field_changes=[
                FieldChange(field="field1", old="value1_1", new="value1_2"),
                FieldChange(field="field2", old="value2_1", new="value2_2"),
            ],
        )

        change_2 = ModelChange(
            date=timezone.datetime(2020, 1, 1, 0, 0, 0, 2),
            user="user1",
            entity_name="entity1",
            entity_id=1,
            field_changes=[
                FieldChange(field="field3", old="value3_1", new="value3_2"),
            ],
        )

        merged = change_1 + change_2

        self.assertEqual(
            merged,
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 0),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field1", old="value1_1", new="value1_2"),
                    FieldChange(field="field2", old="value2_1", new="value2_2"),
                    FieldChange(field="field3", old="value3_1", new="value3_2"),
                ],
            ),
        )

    def test_add_changes_for_existing_field(self):
        change_1 = ModelChange(
            date=timezone.datetime(2020, 1, 1, 0, 0, 0, 0),
            user="user1",
            entity_name="entity1",
            entity_id=1,
            field_changes=[
                FieldChange(field="field1", old="value1_1", new="value1_2"),
                FieldChange(field="field2", old="value2_1", new="value2_2"),
                FieldChange(field="field3", old="value3_1", new="value3_1"),
            ],
        )

        change_2 = ModelChange(
            date=timezone.datetime(2020, 1, 1, 0, 0, 0, 2),
            user="user1",
            entity_name="entity1",
            entity_id=1,
            field_changes=[
                FieldChange(field="field3", old="value3_2", new="value3_3"),
            ],
        )

        merged = change_1 + change_2

        self.assertEqual(
            merged,
            ModelChange(
                date=timezone.datetime(2020, 1, 1, 0, 0, 0, 0),
                user="user1",
                entity_name="entity1",
                entity_id=1,
                field_changes=[
                    FieldChange(field="field1", old="value1_1", new="value1_2"),
                    FieldChange(field="field2", old="value2_1", new="value2_2"),
                    FieldChange(field="field3", old="value3_1", new="value3_3"),
                ],
            ),
        )
