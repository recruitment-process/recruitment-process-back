import base64
from datetime import date

from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField
from recruitment.constants import (
    CANDIDATE_STATUS,
    EDUCATION,
    EMPLOYMENT_TYPE,
    EXPERIENCE,
    FUNNEL_STATUS,
    INTERVIEW_STATUS,
    SCHEDULE_WORK,
    VACANCY_STATUS,
)
from recruitment.models import (
    ApplicantResume,
    Candidate,
    Comment,
    Company,
    Education,
    FunnelStage,
    Note,
    Skills,
    SkillStack,
    SubStage,
    Vacancy,
    WorkExperience,
)
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    EmailField,
    FileField,
    ModelSerializer,
    MultipleChoiceField,
    PrimaryKeyRelatedField,
    Serializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
)
from users.models import User
from users.validators import custom_validate_email

from .constants import MAX_AGE, MIN_AGE
from .utils import (
    DateOnlyField,
    get_display_values,
    get_salary_expectations,
    get_salary_range,
)


class Base64PDFField(FileField):
    """Кастомное поле для загрузки pdf файлов."""

    def to_internal_value(self, data):
        """
        Функция декодирования файла из base64.

        Возвращает адрес с нужным файлом из каталога media/candidates/.
        """
        if isinstance(data, str) and data.startswith("data:application/pdf"):
            format, pdfstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(pdfstr), name="temp." + ext)

        return super().to_internal_value(data)


class UserSignupSerializer(ModelSerializer):
    """Сериализатор пользователя при регистрации."""

    password = CharField(max_length=128)
    email = EmailField(max_length=256)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def to_representation(self, instance):
        """Изменение возвращаемого ответа сериализатора."""
        return {
            "id": instance.id,
        }

    def create(self, validated_data):
        """Создание пользователя в БД."""
        return User.objects.create_user(
            validated_data["email"], validated_data["password"]
        )

    def validate_email(self, value):
        """Валидация email."""
        return custom_validate_email(value)

    def validate_password(self, value):
        """Валидация пароля."""
        validate_password(value)
        return value

    def validate(self, data):
        """Проверка на существование пользователя с email."""
        email = data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Пользователь с адресом {email} уже существует")
        return data


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User."""

    photo = Base64ImageField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "photo",
            "phone_number",
            "email",
            "is_hr",
        )


class ChangePasswordSerializer(Serializer):
    """Сериализатор смены пароля."""

    old_password = CharField(required=True)
    new_password_1 = CharField(required=True)
    new_password_2 = CharField(required=True)

    def validate_new_password_1(self, value):
        """Валидация пароля."""
        validate_password(value)
        return value

    def validate(self, data):
        """Проверка на равенство паролей."""
        new_password_1 = data.get("new_password_1")
        new_password_2 = data.get("new_password_2")
        if not new_password_1 == new_password_2:
            raise ValidationError("Новые пароли не совпадают!")
        return data


class EducationSerializer(ModelSerializer):
    """Сериализатор для модели Education."""

    class Meta:
        model = Education
        fields = (
            "id",
            "educational_institution",
            "faculty",
            "specialization",
            "graduation",
            "resume",
        )


class CompanySerializer(ModelSerializer):
    """Сериализатор для модели Company."""

    logo = Base64ImageField()

    class Meta:
        model = Company
        fields = (
            "id",
            "company_title",
            "about_company",
            "company_address",
            "website",
            "email",
            "phone_number",
            "link_hr",
            "logo",
        )


class CompanyShortSerializer(ModelSerializer):
    """Сериализатор для краткой версии модели Company."""

    class Meta:
        model = Company
        fields = ("id", "company_title", "website")


class WorkExperienceSerializer(ModelSerializer):
    """Сериализатор карточки опыта работы."""

    experience_length = SerializerMethodField()

    class Meta:
        model = WorkExperience
        fields = (
            "start_date",
            "end_date",
            "position",
            "organization",
            "experience_length",
        )

    def get_experience_length(self, obj):
        """
        Функция для вычисления продолжительности работы.

        Возвращает количество месяцев и лет работы.
        """
        if obj.end_date:
            experience_length = (obj.end_date - obj.start_date).days / 30
        else:
            today = date.today()
            experience_length = (today - obj.start_date).days / 30
        years = experience_length // 12
        months = experience_length % 12
        return f"{int(years)} года/лет и {round(months)} месяца(ев)"


class SkillsSerializer(ModelSerializer):
    """Сериализатор для модели Skills."""

    class Meta:
        model = Skills
        fields = ["name"]


class SkillStackSerializer(ModelSerializer):
    """Сериализатор для модели SkillStack."""

    skill_stack = SkillsSerializer()

    class Meta:
        model = SkillStack
        fields = ["skill_stack", "skill_stack_time"]

    def create(self, validated_data):
        """
        Создает новый объект SkillStack, связанный с объектом Skills.

        Если объект Skills с заданным именем не существует, он создается.
        """
        skill_data = validated_data.pop("skill_stack")
        skill, created = Skills.objects.get_or_create(**skill_data)
        return SkillStack.objects.create(skill_stack=skill, **validated_data)


class VacancySerializer(ModelSerializer):
    """Сериализатор карточки вакансии."""

    company = CompanyShortSerializer()
    author = StringRelatedField(read_only=True)
    schedule_work = MultipleChoiceField(choices=SCHEDULE_WORK)
    employment_type = MultipleChoiceField(choices=EMPLOYMENT_TYPE)
    education = ChoiceField(choices=EDUCATION)
    pub_date = DateOnlyField(read_only=True)
    candidates_count = SerializerMethodField()
    skill_stack = SkillStackSerializer(many=True)
    vacancy_status = ChoiceField(choices=VACANCY_STATUS)

    class Meta:
        model = Vacancy
        fields = (
            "id",
            "vacancy_title",
            "company",
            "author",
            "required_experience",
            "employment_type",
            "schedule_work",
            "salary",
            "city",
            "education",
            "pub_date",
            "job_conditions",
            "job_responsibilities",
            "skill_stack",
            "vacancy_status",
            "deadline",
            "candidates_count",
        )
        read_only_fields = ("author",)

    def create(self, validated_data):
        """
        Создает новый объект Vacancy, связанный с объектами Company и SkillStack.

        Если объекты Company или SkillStack не существуют, они создаются.
        """
        skill_stack_data = validated_data.pop("skill_stack")
        company_data = validated_data.pop("company")
        company, created = Company.objects.update_or_create(**company_data)
        vacancy = Vacancy.objects.create(company=company, **validated_data)
        for skill_data in skill_stack_data:
            skill_stack_serializer = SkillStackSerializer(data=skill_data)
            if skill_stack_serializer.is_valid():
                skill_stack_serializer.save(vacancy=vacancy)
        return vacancy

    def update(self, instance, validated_data):
        """
        Функция для обновления экземпляра Company, SkillStack.

        Возвращает обновленный экземпляр Vacancy.
        """
        company_data = validated_data.pop("company")
        Company.objects.filter(id=instance.company.id).update(**company_data)
        skill_stack_data_list = validated_data.pop("skill_stack")
        instance.skill_stack.clear()
        for skill_stack_data in skill_stack_data_list:
            skill_stack, created = SkillStack.objects.update_or_create(
                **skill_stack_data
            )
            instance.skill_stack.add(skill_stack)

        return super().update(instance, validated_data)

    def get_candidates_count(self, obj):
        """Подсчет количества кандидатов на вакансию."""
        return obj.candidates.count()


class VacanciesSerializer(ModelSerializer):
    """Сериализатор для просмотра карточек вакансий."""

    company = StringRelatedField(read_only=True)
    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()
    salary_range = SerializerMethodField()
    candidates_count = SerializerMethodField()
    skill_stack = StringRelatedField(many=True, read_only=True)
    vacancy_status = SerializerMethodField()
    required_experience = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "id",
            "vacancy_title",
            "company",
            "required_experience",
            "employment_type",
            "schedule_work",
            "salary_range",
            "city",
            "skill_stack",
            "deadline",
            "candidates_count",
            "vacancy_status",
        )

    def get_schedule_work(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля schedule_work.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля employment_type.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)

    def get_salary_range(self, obj):
        """Функция преобразования вывода информации для поля salary."""
        return get_salary_range(obj)

    def get_vacancy_status(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля vacancy_status.
        """
        return get_display_values(obj.vacancy_status, VACANCY_STATUS)[0]

    def get_required_experience(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля required_experience.
        """
        return get_display_values(obj.required_experience, EXPERIENCE)[0]

    def get_candidates_count(self, obj):
        """Подсчет количества кандидатов на вакансию."""
        return obj.candidates.count()


class ResumeSerializer(ModelSerializer):
    """Сериализатор карточки резюме."""

    schedule_work = MultipleChoiceField(choices=SCHEDULE_WORK)
    employment_type = MultipleChoiceField(choices=EMPLOYMENT_TYPE)
    education = ChoiceField(choices=EDUCATION)
    age = SerializerMethodField()
    salary_expectations = SerializerMethodField()
    work_experiences = WorkExperienceSerializer(many=True)
    pub_date = DateOnlyField(read_only=True)

    class Meta:
        model = ApplicantResume
        fields = (
            "applicant",
            "job_title",
            "employment_type",
            "schedule_work",
            "salary_expectations",
            "working_trip",
            "phone_number",
            "pub_date",
            "education",
            "town",
            "citizenship",
            "bday",
            "age",
            "work_experiences",
            "about_me",
            "current_company",
            "current_job",
        )

    def get_age(self, obj):
        """Функция для подсчета возраста соискателя."""
        today = date.today()
        born = obj.bday
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    def validate_bday(self, obj):
        """Функция валидации даты рождения соискателя."""
        today = date.today()
        if not (MAX_AGE > (today.year - obj.year) > MIN_AGE):
            raise ValidationError("Проверьте дату рождения!")
        return obj

    def get_salary_expectations(self, obj):
        """Функция преобразования вывода информации для поля salary_expectations."""
        return get_salary_expectations(obj)


class ResumesSerializer(ModelSerializer):
    """Сериализатор для карточек резюме."""

    class Meta:
        model = ApplicantResume
        fields = (
            "applicant",
            "job_title",
            "work_experiences",
            "current_company",
        )


class CandidateSerializer(ModelSerializer):
    """Сериализатор для кандидата."""

    education = ChoiceField(choices=EDUCATION)
    age = SerializerMethodField()
    interview_status = ChoiceField(choices=INTERVIEW_STATUS, required=False)
    candidate_status = ChoiceField(choices=CANDIDATE_STATUS)
    salary_expectations = SerializerMethodField()
    schedule_work = MultipleChoiceField(choices=SCHEDULE_WORK)
    employment_type = MultipleChoiceField(choices=EMPLOYMENT_TYPE)
    work_experiences = ChoiceField(choices=EXPERIENCE)
    resume = Base64PDFField()
    photo = Base64ImageField()
    custom_status = CharField(required=False, allow_null=True)
    pub_date = DateOnlyField(read_only=True)
    vacancy = StringRelatedField(read_only=True)

    class Meta:
        model = Candidate
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "bday",
            "age",
            "city",
            "last_job",
            "cur_position",
            "salary_expectations",
            "vacancy",
            "phone_number",
            "email",
            "telegram",
            "portfolio",
            "resume",
            "photo",
            "employment_type",
            "schedule_work",
            "work_experiences",
            "education",
            "candidate_status",
            "interview_status",
            "custom_status",
            "pub_date",
        )

    def validate(self, data):
        """Валидация полей на одновременное заполнение."""
        if data.get("custom_status") and data.get("interview_status"):
            raise ValidationError("Нельзя заполнить оба поля одновременно.")
        return data

    def get_age(self, obj):
        """Функция для подсчета возраста соискателя."""
        today = date.today()
        born = obj.bday
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    def validate_bday(self, obj):
        """Функция валидации даты рождения соискателя."""
        today = date.today()
        if not (MAX_AGE > (today.year - obj.year) > MIN_AGE):
            raise ValidationError("Проверьте дату рождения!")
        return obj

    def get_salary_expectations(self, obj):
        """Функция преобразования вывода информации для поля salary_expectations."""
        return get_salary_expectations(obj)


class CandidatesSerializer(ModelSerializer):
    """Сериализатор для карточек кандидатов."""

    interview_status = SerializerMethodField()
    candidate_status = SerializerMethodField()
    custom_status = CharField(required=False)
    work_experiences = SerializerMethodField()

    class Meta:
        model = Candidate
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "cur_position",
            "work_experiences",
            "last_job",
            "interview_status",
            "custom_status",
            "candidate_status",
        )

    def get_interview_status(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля interview_status.
        """
        return get_display_values([obj.interview_status], INTERVIEW_STATUS)[0]

    def get_work_experiences(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля work_experiences.
        """
        return get_display_values(obj.work_experiences, EXPERIENCE)[0]

    def get_candidate_status(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля candidate_status.
        """
        return get_display_values(obj.candidate_status, CANDIDATE_STATUS)[0]


class SubStageSerializer(ModelSerializer):
    """Сериализатор для подэтапов воронок."""

    stage = StringRelatedField(read_only=True)
    status = ChoiceField(choices=FUNNEL_STATUS)

    class Meta:
        model = SubStage
        fields = (
            "id",
            "stage",
            "name",
            "date",
            "status",
        )


class FunnelSerializer(ModelSerializer):
    """Сериализатор для воронок кандидатов."""

    candidate = StringRelatedField(read_only=True)
    status = ChoiceField(choices=FUNNEL_STATUS)

    class Meta:
        model = FunnelStage
        fields = (
            "id",
            "candidate",
            "name",
            "date",
            "status",
        )


class FunnelDetailSerializer(ModelSerializer):
    """Сериализатор для воронок c подэтапами кандидатов."""

    candidate = StringRelatedField(read_only=True)
    substages = SubStageSerializer(many=True, required=False)
    status = ChoiceField(choices=FUNNEL_STATUS)

    def create(self, validated_data):
        """Функция создания воронки Funnel."""
        if "substages" not in self.initial_data:
            funnel = FunnelStage.objects.create(**validated_data)
            return funnel
        substages = validated_data.pop("substages")
        funnel = FunnelStage.objects.create(**validated_data)
        for substage in substages:
            SubStage.objects.create(stage=funnel, **substage)
        return funnel

    class Meta:
        model = FunnelStage
        fields = (
            "id",
            "candidate",
            "name",
            "date",
            "status",
            "substages",
        )


class NoteSerializer(ModelSerializer):
    """Сериализатор для заметок."""

    author_id = PrimaryKeyRelatedField(read_only=True, source="author")

    class Meta:
        fields = (
            "id",
            "candidate",
            "text",
            "author_id",
            "pub_date",
        )
        model = Note
        read_only_fields = ("candidate",)


class CommentSerializer(ModelSerializer):
    """Сериализатор для ответов."""

    author_id = PrimaryKeyRelatedField(read_only=True, source="author")
    note_id = PrimaryKeyRelatedField(read_only=True, source="note")

    class Meta:
        fields = (
            "id",
            "note_id",
            "text",
            "author_id",
            "pub_date",
        )
        model = Comment
        read_only_fields = ("note_id",)


class NoteDetailSerializer(ModelSerializer):
    """Сериализатор для заметок с комментариями."""

    author_id = PrimaryKeyRelatedField(read_only=True, source="author")
    comments = CommentSerializer(
        many=True,
    )

    class Meta:
        fields = (
            "id",
            "candidate",
            "text",
            "author_id",
            "pub_date",
            "comments",
        )
        model = Note
        read_only_fields = ("candidate",)
