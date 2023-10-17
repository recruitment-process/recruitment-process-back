import datetime as dt

from django.core.validators import RegexValidator

EMPLOYMENT_TYPE = (
    ("PO", "Полная"),
    ("CH", "Частичная"),
    ("PR", "Проектная"),
    ("ST", "Стажировка"),
)

SCHEDULE_WORK = (
    ("P", "Офис"),
    ("G", "Гибрид"),
    ("U", "Удаленный"),
    ("W", "Вахтовый"),
)

EDUCATION = (
    ("SR", "Среднее"),
    ("VN", "Высшее неполное"),
    ("VS", "Высшее"),
    ("RC", "Переподготовка"),
)

EXPERIENCE = (
    ("1", "Без опыта"),
    ("2", "1-3 года"),
    ("3", "3-5 лет"),
    ("4", "Более 5 лет"),
)

VACANCY_STATUS = (
    ("A", "activeVacancies"),
    ("F", "completedVacancies"),
    ("D", "draftVacancies"),
)

CANDIDATE_STATUS = (
    ("A", "activeCandidates"),
    ("F", "favoritesCandidates"),
    ("R", "rejectedCandidates"),
    ("T", "trialCandidates"),
    ("S", "standbyCandidates"),
)

INTERVIEW_STATUS = (
    ("PS", "Первичный скрининг"),
    ("IHR", "Интервью с HR"),
    ("IHD", "Интервью с руководителем"),
    ("TT", "Тестовое задание"),
    ("CTT", "Выполнил тестовое задание"),
    ("IT", "Интервью с командой"),
    ("OFFER", "Оффер"),
    ("OC", "Оффер принят"),
)

FUNNEL_STATUS = (
    ("1", "Создан"),
    ("2", "Пройден"),
    ("3", "Провален"),
)

PHONE_NUMBER_REGEX = RegexValidator(regex=r"^\+?1?\d{8,15}$")

FUNNEL_STATUS = (
    ("1", "Создан"),
    ("2", "Пройден"),
    ("3", "Провален"),
)

PHONE_NUMBER_REGEX = RegexValidator(regex=r"^\+?1?\d{8,15}$")
VALID_TELEGRAM_REGEX = RegexValidator(regex=r"^@[a-zA-Z0-9_-]+$")
DEADLINE = dt.date.today() + dt.timedelta(days=30)
