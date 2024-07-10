from django.db import models
from category.models import Category, SubCategory
from user.models import User


class Presentation(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'presentation'

    def __str__(self):
        return f'{self.name}'


class CoAuthor(models.Model):
    name = models.CharField(max_length=128)
    institution = models.CharField(max_length=256)

    class Meta:
        db_table = 'coauthor'

    def __str__(self):
        return f'{self.name} - {self.institution}'


class KeyWord(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'keyword'

    def __str__(self):
        return f'{self.name}'


class Status(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'status'

    def __str__(self):
        return f'{self.name}'


class AbstractBase(models.Model):
    title = models.CharField(max_length=256)
    ethic = models.BooleanField(default=False)
    presentation = models.ForeignKey(Presentation, null=False, blank=False, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, null=False, on_delete=models.PROTECT)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    coauthor = models.ManyToManyField(CoAuthor)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField(null=True, blank=True)
    keyword = models.ManyToManyField(KeyWord)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Abstract(AbstractBase):
    introduction = models.TextField(default=None, null=True, blank=True)
    methodology = models.TextField(default=None, null=True, blank=True)
    result = models.TextField(default=None, null=True, blank=True)
    conclusion = models.TextField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'abstract'

    def __str__(self):
        return f'{self.title}'


class ClinicCaseAbstract(AbstractBase):
    introduction = models.TextField(default=None, null=True, blank=True)
    resume = models.TextField(default=None, null=True, blank=True)
    discussion = models.TextField(default=None, null=True, blank=True)
    conclusion = models.TextField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'clinic_case'

    def __str__(self):
        return f'{self.title}'


class ProgrammaticEvaluationAbstract(AbstractBase):
    introduction = models.TextField(default=None, null=True, blank=True)
    intervention = models.TextField(default=None, null=True, blank=True)
    methodology = models.TextField(default=None, null=True, blank=True)
    result = models.TextField(default=None, null=True, blank=True)
    lessons = models.TextField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'programmatic_evaluation'

    def __str__(self):
        return f'{self.title}'


class AbstractReviewerBase(models.Model):
    reviewer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    title = models.TextField(default=None, null=True, blank=True)
    presentation = models.ForeignKey(Presentation, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True, default=None)
    subcategory = models.TextField(null=True, blank=True, default=None)
    status = models.ForeignKey(
        Status,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        default=Status.objects.get_or_create(name="Em Revisão")[0].id
    )
    classification = models.SmallIntegerField(default=0, blank=True)
    keyword = models.TextField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractReviewer(AbstractReviewerBase):
    abstract = models.ForeignKey(Abstract, null=False, blank=False, on_delete=models.CASCADE)
    introduction = models.TextField(default=None, null=True, blank=True)
    methodology = models.TextField(default=None, null=True, blank=True)
    result = models.TextField(default=None, null=True, blank=True)
    conclusion = models.TextField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'abstractReviewer'
        unique_together = [['reviewer', 'abstract']]

    def __str__(self):
        return (f'Reviewer: {self.reviewer.first_user_name} {self.reviewer.last_user_name} - '
                f'Resume: {self.abstract.title}')


class ClinicCaseAbstractReviewer(AbstractReviewerBase):
    clinicCase = models.ForeignKey(ClinicCaseAbstract, null=False, blank=False, on_delete=models.CASCADE)
    introduction = models.TextField(default=None, null=True, blank=True)
    resume = models.TextField(default=None, null=True, blank=True)
    discussion = models.TextField(default=None, null=True, blank=True)
    conclusion = models.TextField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'clinicReviewer'
        unique_together = [['reviewer', 'clinicCase']]

    def __str__(self):
        return (f'Reviewer: {self.reviewer.first_user_name} {self.reviewer.last_user_name} - '
                f'Resume: {self.clinicCase.title}')


class ProgrammaticEvaluationAbstractReviewer(AbstractReviewerBase):
    programmaticEvaluation = models.ForeignKey(
        ProgrammaticEvaluationAbstract,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    introduction = models.TextField(default=None, null=True, blank=True)
    intervention = models.TextField(default=None, null=True, blank=True)
    methodology = models.TextField(default=None, null=True, blank=True)
    result = models.TextField(default=None, null=True, blank=True)
    lessons = models.TextField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'programmaticReviewer'
        unique_together = [['reviewer', 'programmaticEvaluation']]

    def __str__(self):
        return (f'Reviewer: {self.reviewer.first_user_name} {self.reviewer.last_user_name} - '
                f'Resume: {self.programmaticEvaluation.title}')
