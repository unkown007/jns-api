from django.contrib import admin
from .models import (
    Status,
    KeyWord,
    Abstract,
    CoAuthor,
    Presentation,
    AbstractReviewer,
    ClinicCaseAbstract,
    ClinicCaseAbstractReviewer,
    ProgrammaticEvaluationAbstract,
    ProgrammaticEvaluationAbstractReviewer
)

admin.site.register(Status)
admin.site.register(KeyWord)
admin.site.register(Abstract)
admin.site.register(CoAuthor)
admin.site.register(Presentation)
admin.site.register(AbstractReviewer)
admin.site.register(ClinicCaseAbstract)
admin.site.register(ClinicCaseAbstractReviewer)
admin.site.register(ProgrammaticEvaluationAbstract)
admin.site.register(ProgrammaticEvaluationAbstractReviewer)
