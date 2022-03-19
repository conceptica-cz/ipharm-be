from django.test import TestCase
from ipharm.models.pharmacological_plans import (
    PharmacologicalPlanComment,
    VerificationNumberLimitIsReached,
)

from factories.ipharm import (
    PharmacologicalPlanCommentFactory,
    PharmacologicalPlanFactory,
)


class PharmacologicalPlanTest(TestCase):
    def test_that_medical_procedure_is_created(self):
        """
        Medical procedure 05753 is created when a new PharmacologicalPlan is created.
        """
        plan = PharmacologicalPlanFactory()
        self.assertEqual(plan.medical_procedure.code, "05753")


class PharmacologicalPlanCommentTest(TestCase):
    def test_that_medical_procedure_is_created_for_type_verification(self):
        """
        Medical procedure 05755 is created when a new PharmacologicalPlanComment
        with comment_type "verification" is created.
        """
        plan = PharmacologicalPlanCommentFactory(comment_type="verification")
        self.assertEqual(plan.medical_procedure.code, "05755")

    def test_that_medical_procedure_is_not_created_for_type_comment(self):
        """
        Medical procedure 05755 is created when a new PharmacologicalPlanComment
        with comment_type "verification" is created.
        """
        plan = PharmacologicalPlanCommentFactory(comment_type="comment")
        self.assertEqual(plan.medical_procedure, None)

    def test_that_only_two_verification_comments_can_be_created(self):
        """
        Only two comments with comment_type "verification" can be created for a plan.
        """
        plan = PharmacologicalPlanFactory()
        PharmacologicalPlanComment.objects.all().delete()
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="verification"
        )
        comment = PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="verification"
        )
        comment.save()
        with self.assertRaises(VerificationNumberLimitIsReached):
            PharmacologicalPlanCommentFactory(
                pharmacological_plan=plan, comment_type="verification"
            )
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="comment"
        )
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="comment"
        )
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="comment"
        )

        self.assertEqual(
            PharmacologicalPlanComment.objects.filter(comment_type="comment").count(), 3
        )
        self.assertEqual(
            PharmacologicalPlanComment.objects.filter(
                comment_type="verification"
            ).count(),
            2,
        )
