from datetime import date

from django.core.exceptions import ValidationError
from django.db import DataError
from django.test import TestCase
from recruitment.models import (
    Candidate,
    Event,
    FunnelStage,
    Skills,
    SkillStack,
    SubStage,
    WorkExperience,
)


class SkillsModelTest(TestCase):
    """Тестирование модели Skills."""

    def test_skills_model_str(self):
        """Тестирование метода __str__ модели Skills."""
        skill = Skills(name="Python")
        self.assertEqual(str(skill), "Python")

    def test_skills_model_max_length(self):
        """Тестирование ограничения max_length для поля name в модели Skills."""
        with self.assertRaises(DataError):
            skills = Skills(name="P" * 51)
            skills.save()


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


class CandidateModelTest(TestCase):
    """Тестирование модели Candidate."""

    def test_candidate_creation(self):
        """Тестирование метода __str__."""
        candidate = Candidate(
            first_name="Иван",
            last_name="Иванов",
            bday=date(1990, 1, 1),
            city="Москва",
            email="ivan@example.com",
        )
        self.assertEqual(candidate.__str__(), "Иванов")


class EventModelTest(TestCase):
    """Тестирование модели Event."""

    def test_event_model_str(self):
        """Тестирование метода __str__."""
        event = Event(title="Собеседование", start_date=date(2023, 1, 1))
        self.assertEqual(event.__str__(), "Собеседование")


class FunnelStageModelTest(TestCase):
    """Тестирование модели FunnelStage."""

    def test_funnel_stage_creation(self):
        """Тестирование метода __str__."""
        funnel_stage = FunnelStage(name="Собеседование", date=date(2023, 1, 1))
        self.assertEqual(funnel_stage.__str__(), "Собеседование")


class SubStageModelTest(TestCase):
    """Тестирование модели SubStage."""

    def test_sub_stage_creation(self):
        """Тестирование метода __str__."""
        sub_stage = SubStage(name="Техническое собеседование", date=date(2023, 2, 1))
        self.assertEqual(sub_stage.__str__(), "Техническое собеседование")
