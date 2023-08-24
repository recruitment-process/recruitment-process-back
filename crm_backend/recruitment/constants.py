from django.core.validators import RegexValidator

EMPLOYMENT_TYPE = (
    ("PO", "Полная"),
    ("CH", "Частичная"),
    ("PR", "Проектная"),
    ("ST", "Стажировка"),
    ("VO", "Волонтерство"),
)

SCHEDULE_WORK = (
    ("P", "Полный день"),
    ("S", "Сменный график"),
    ("G", "Гибкий график"),
    ("U", "Удаленная работа"),
    ("W", "Вахтовый метод"),
)

RELOCATION = (
    ("VZ", "Возможен"),
    ("NV", "Невозможен"),
    ("GL", "Желателен"),
    ("NG", "Нежелателен"),
)

GENDER = (
    ("M", "Мужской"),
    ("W", "Женский"),
)

EDUCATION = (
    ("SN", "Среднее неполное"),
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
    ("A", "Активные"),
    ("F", "Завернешшые"),
    ("D", "Черновики"),
)

INTERVIEW_STATUS = (
    ("PS", "Первичный скрининг"),
    ("IHR", "Интервью с HR"),
    ("IHD", "Интервью с руководителем"),
    ("TT", "Тестовое задание"),
    ("CTT", "Выполнил тестовое задание"),
    ("IT", "Интервью с командой"),
    ("O", "Оффер"),
)

FUNNEL_STATUS = (
    ("1", "Создан"),
    ("2", "Пройден"),
    ("3", "Провален"),
)

PHONE_NUMBER_REGEX = RegexValidator(regex=r"^\+?1?\d{8,15}$")
