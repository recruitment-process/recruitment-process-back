from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from recruitment.models import Skills, SkillStack, WorkExperience


class SkillsModelTest(TestCase):
    """Тестирование модели Skills."""

    def test_skills_model_str(self):
        """Тестирование метода __str__ модели Skills."""
        skill = Skills(name="Python")
        self.assertEqual(str(skill), "Python")


class SkillStackModelTest(TestCase):
    """Тестирование модели SkillStack."""

    def test_skillstack_model_str(self):
        """Тестирование метода __str__ модели SkillStack."""
        skill = Skills(name="Python")
        skillstack = SkillStack(skill_stack=skill, skill_stack_time=2)
        self.assertEqual(str(skillstack), "Python - 2 года")


class WorkExperienceModelTest(TestCase):
    """Тестирование модели WorkExperience."""

    def test_workexperience_model_str(self):
        """Тестирование метода __str__ модели WorkExperience."""
        experience = WorkExperience(
            start_date=date(2020, 1, 1),
            end_date=date(2022, 12, 31),
            position="Developer",
            organization="ABC Inc",
        )
        self.assertEqual(str(experience), "Developer - ABC Inc")

    def test_workexperience_model_clean_valid_dates(self):
        """Тестирование метода clean с корректными датами."""
        experience = WorkExperience(
            start_date=date(2020, 1, 1),
            end_date=date(2022, 12, 31),
        )
        experience.clean()

    def test_workexperience_model_clean_invalid_dates(self):
        """Тестирование метода clean с некорректными датами."""
        experience = WorkExperience(
            start_date=date(2023, 1, 1),
            end_date=date(2022, 12, 31),
        )
        with self.assertRaises(ValidationError):
            experience.clean()
