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

RELOCATION = (
    ("VZ", "Возможен"),
    ("NV", "Невозможен"),
    ("GL", "Желателен"),
    ("NG", "Нежелателен"),
)

GENDER = (
    ("MAN", "Мужской"),
    ("WOMAN", "Женский"),
)

EDUCATION = (
    ("SR", "Среднее"),
    ("SP", "Среднее профессиональное"),
    ("VN", "Высшее неполное"),
    ("VS", "Высшее"),
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

INTERVIEW_STATUS = (
    ("PS", "Первичный скрининг"),
    ("IHR", "Интервью с HR"),
    ("IHD", "Интервью с руководителем"),
    ("TT", "Тестовое задание"),
    ("CTT", "Выполнил тестовое задание"),
    ("IT", "Интервью с командой"),
    ("OFFER", "Оффер"),
)

FUNNEL_STATUS = (
    ("1", "Создан"),
    ("2", "Пройден"),
    ("3", "Провален"),
)

PHONE_NUMBER_REGEX = RegexValidator(regex=r"^\+?1?\d{8,15}$")
