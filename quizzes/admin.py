from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from quizzes.models import TruthOrDareQuestion, Wish, Prediction


class PredictionResource(ModelResource):
    class Meta:
        model = Prediction


@admin.register(Prediction)
class PredictionAdmin(ImportExportModelAdmin):
    resource_class = PredictionResource
    search_fields = ('text',)
    list_display = ('__str__',)


class WishResource(ModelResource):
    class Meta:
        model = Wish


@admin.register(Wish)
class WishAdmin(ImportExportModelAdmin):
    resource_class = WishResource
    search_fields = ('text',)
    list_display = ('__str__',)


class TruthOrDareResource(ModelResource):
    class Meta:
        model = TruthOrDareQuestion


@admin.register(TruthOrDareQuestion)
class TruthOrDareQuestionAdmin(ImportExportModelAdmin):
    list_filter = ('type',)
    list_display = ('text', 'type')
    resource_class = TruthOrDareResource
