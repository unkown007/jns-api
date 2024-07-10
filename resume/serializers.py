from rest_framework import serializers

from category.models import Category, SubCategory
from category.serializers import CategorySerializer, SubCategorySerializer
from user.serializers import UserLightSerializer, UserSerializer
from .models import (
    Presentation,
    CoAuthor,
    KeyWord,
    Status,
    Abstract,
    AbstractReviewer,
    ClinicCaseAbstract,
    ClinicCaseAbstractReviewer,
    ProgrammaticEvaluationAbstract,
    ProgrammaticEvaluationAbstractReviewer
)
from user.models import User


class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = '__all__'


class CoAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoAuthor
        fields = '__all__'


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class AbstractSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True, read_only=True)
    presentation = PresentationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    author = UserSerializer(read_only=True)
    coauthor = CoAuthorSerializer(many=True, read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Abstract
        fields = '__all__'


class ClinicCaseAbstractSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True, read_only=True)
    presentation = PresentationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    author = UserSerializer(read_only=True)
    coauthor = CoAuthorSerializer(many=True, read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = ClinicCaseAbstract
        fields = '__all__'


class ProgrammaticEvaluationAbstractSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True, read_only=True)
    presentation = PresentationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    author = UserSerializer(read_only=True)
    coauthor = CoAuthorSerializer(many=True, read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = ProgrammaticEvaluationAbstract
        fields = '__all__'


class AbstractAnonymSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True, read_only=True)
    author = UserLightSerializer(read_only=True)
    presentation = PresentationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Abstract
        exclude = ['coauthor']


class ClinicCaseAbstractAnonymSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True, read_only=True)
    author = UserLightSerializer(read_only=True)
    presentation = PresentationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = ClinicCaseAbstract
        exclude = ['coauthor']


class ProgrammaticEvaluationAbstractAnonymSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True, read_only=True)
    author = UserLightSerializer(read_only=True)
    presentation = PresentationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = ProgrammaticEvaluationAbstract
        exclude = ['coauthor']


class AbstractLightSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    author = UserLightSerializer(read_only=True)

    class Meta:
        model = Abstract
        fields = [
            'id',
            'title',
            'author'
        ]


class AbstractAddSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True)
    presentation = serializers.PrimaryKeyRelatedField(queryset=Presentation.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    coauthor = CoAuthorSerializer(many=True)
    # status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = Abstract
        fields = '__all__'

    def create(self, validated_data):
        coauthors_data = validated_data.pop('coauthor')
        keywords_data = validated_data.pop('keyword')

        abstract, _ = Abstract.objects.get_or_create(**validated_data)

        for coauthor_data in coauthors_data:
            coauthor, _ = CoAuthor.objects.get_or_create(**coauthor_data)
            abstract.coauthor.add(coauthor)

        for keyword_data in keywords_data:
            keyword, _ = KeyWord.objects.get_or_create(**keyword_data)
            abstract.keyword.add(keyword)

        abstract.status = Status.objects.get_or_create(name="Em validação")[0]
        abstract.save()

        return abstract

    def update(self, instance, validated_data):
        coauthors_data = validated_data.pop('coauthor')
        keywords_data = validated_data.pop('keyword')

        coauthors = [CoAuthor.objects.get_or_create(**coauthor_data)[0] for coauthor_data in coauthors_data]
        keywords = [KeyWord.objects.get_or_create(**keyword_data)[0] for keyword_data in keywords_data]

        instance.title = validated_data.get('title', instance.title)
        instance.introduction = validated_data.get("introduction", instance.introduction)
        # instance.objective = validated_data.get("objective", instance.objective)
        instance.ethic = validated_data.get("ethic", instance.ethic)
        instance.methodology = validated_data.get("methodology", instance.methodology)
        instance.result = validated_data.get("result", instance.result)
        instance.conclusion = validated_data.get("conclusion", instance.conclusion)

        instance.presentation = validated_data.get("presentation")
        instance.category = validated_data.get("category")
        instance.subcategory = validated_data.get("subcategory")
        instance.author = validated_data.get("author", instance.author)

        instance.coauthor.set(coauthors)
        instance.keyword.set(keywords)
        instance.save()

        keywords_ids = list(set(Abstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids1 = list(set(ClinicCaseAbstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids2 = list(set(ProgrammaticEvaluationAbstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids = keywords_ids + keywords_ids1 + keywords_ids2
        KeyWord.objects.all().exclude(id__in=keywords_ids).delete()

        coauthors_ids = list(set(Abstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids1 = list(set(ClinicCaseAbstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids2 = list(set(ProgrammaticEvaluationAbstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids = coauthors_ids + coauthors_ids1 + coauthors_ids2
        CoAuthor.objects.all().exclude(id__in=coauthors_ids).delete()

        return instance


class ClinicCaseAbstractAddSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True)
    presentation = serializers.PrimaryKeyRelatedField(queryset=Presentation.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    coauthor = CoAuthorSerializer(many=True)

    class Meta:
        model = ClinicCaseAbstract
        fields = "__all__"

    def create(self, validated_data):
        coauthors_data = validated_data.pop('coauthor')
        keywords_data = validated_data.pop('keyword')

        abstract, _ = ClinicCaseAbstract.objects.get_or_create(**validated_data)

        for coauthor_data in coauthors_data:
            coauthor, _ = CoAuthor.objects.get_or_create(**coauthor_data)
            abstract.coauthor.add(coauthor)

        for keyword_data in keywords_data:
            keyword, _ = KeyWord.objects.get_or_create(**keyword_data)
            abstract.keyword.add(keyword)

        abstract.status = Status.objects.get_or_create(name="Em validação")[0]
        abstract.save()

        return abstract

    def update(self, instance, validated_data):
        coauthors_data = validated_data.pop('coauthor')
        keywords_data = validated_data.pop('keyword')

        coauthors = [CoAuthor.objects.get_or_create(**coauthor_data)[0] for coauthor_data in coauthors_data]
        keywords = [KeyWord.objects.get_or_create(**keyword_data)[0] for keyword_data in keywords_data]

        instance.title = validated_data.get('title', instance.title)
        instance.introduction = validated_data.get("introduction", instance.introduction)
        instance.ethic = validated_data.get("ethic", instance.ethic)
        instance.resume = validated_data.get("resume", instance.resume)
        instance.discussion = validated_data.get("discussion", instance.discussion)
        instance.conclusion = validated_data.get("conclusion", instance.conclusion)

        instance.presentation = validated_data.get("presentation")
        instance.category = validated_data.get("category")
        instance.subcategory = validated_data.get("subcategory")
        instance.author = validated_data.get("author", instance.author)

        instance.coauthor.set(coauthors)
        instance.keyword.set(keywords)
        instance.save()

        keywords_ids = list(set(Abstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids1 = list(set(ClinicCaseAbstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids2 = list(set(ProgrammaticEvaluationAbstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids = keywords_ids + keywords_ids1 + keywords_ids2
        KeyWord.objects.all().exclude(id__in=keywords_ids).delete()

        coauthors_ids = list(set(Abstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids1 = list(set(ClinicCaseAbstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids2 = list(set(ProgrammaticEvaluationAbstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids = coauthors_ids + coauthors_ids1 + coauthors_ids2
        CoAuthor.objects.all().exclude(id__in=coauthors_ids).delete()

        return instance


class ProgrammaticEvaluationAbstractAddSerializer(serializers.ModelSerializer):
    keyword = KeyWordSerializer(many=True)
    presentation = serializers.PrimaryKeyRelatedField(queryset=Presentation.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    coauthor = CoAuthorSerializer(many=True)

    class Meta:
        model = ProgrammaticEvaluationAbstract
        fields = "__all__"

    def create(self, validated_data):
        coauthors_data = validated_data.pop('coauthor')
        keywords_data = validated_data.pop('keyword')

        abstract, _ = ProgrammaticEvaluationAbstract.objects.get_or_create(**validated_data)

        for coauthor_data in coauthors_data:
            coauthor, _ = CoAuthor.objects.get_or_create(**coauthor_data)
            abstract.coauthor.add(coauthor)

        for keyword_data in keywords_data:
            keyword, _ = KeyWord.objects.get_or_create(**keyword_data)
            abstract.keyword.add(keyword)

        abstract.status = Status.objects.get_or_create(name="Em validação")[0]
        abstract.save()

        return abstract

    def update(self, instance, validated_data):
        coauthors_data = validated_data.pop('coauthor')
        keywords_data = validated_data.pop('keyword')

        coauthors = [CoAuthor.objects.get_or_create(**coauthor_data)[0] for coauthor_data in coauthors_data]
        keywords = [KeyWord.objects.get_or_create(**keyword_data)[0] for keyword_data in keywords_data]

        instance.title = validated_data.get('title', instance.title)
        instance.introduction = validated_data.get("introduction", instance.introduction)
        instance.ethic = validated_data.get("ethic", instance.ethic)
        instance.intervention = validated_data.get("intervention", instance.intervention)
        instance.methodology = validated_data.get("methodology", instance.methodology)
        instance.result = validated_data.get("result", instance.result)
        instance.lessons = validated_data.get("lessons", instance.lessons)

        instance.presentation = validated_data.get("presentation")
        instance.category = validated_data.get("category")
        instance.subcategory = validated_data.get("subcategory")
        instance.author = validated_data.get("author", instance.author)

        instance.coauthor.set(coauthors)
        instance.keyword.set(keywords)
        instance.save()

        keywords_ids = list(set(Abstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids1 = list(set(ClinicCaseAbstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids2 = list(set(ProgrammaticEvaluationAbstract.objects.all().values_list("keyword", flat=True)))
        keywords_ids = keywords_ids + keywords_ids1 + keywords_ids2
        KeyWord.objects.all().exclude(id__in=keywords_ids).delete()

        coauthors_ids = list(set(Abstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids1 = list(set(ClinicCaseAbstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids2 = list(set(ProgrammaticEvaluationAbstract.objects.all().values_list("coauthor", flat=True)))
        coauthors_ids = coauthors_ids + coauthors_ids1 + coauthors_ids2
        CoAuthor.objects.all().exclude(id__in=coauthors_ids).delete()

        return instance


class AbstractStatusSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    presentation = serializers.PrimaryKeyRelatedField(queryset=Presentation.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    class Meta:
        model = Abstract
        fields = [
            'status',
            'comment',
            'presentation',
            'category',
            'subcategory'
        ]

    # def update(self, instance, validated_data):
    #     instance.status = validated_data.get("status")
    #     instance.comment = validated_data.get("comment")
    #
    #     instance.save()
    #
    #     return instance


class ClinicCaseAbstractStatusSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    presentation = serializers.PrimaryKeyRelatedField(queryset=Presentation.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    class Meta:
        model = ClinicCaseAbstract
        fields = [
            'status',
            'comment',
            'presentation',
            'category',
            'subcategory'
        ]


class ProgrammaticEvaluationAbstractStatusSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    presentation = serializers.PrimaryKeyRelatedField(queryset=Presentation.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    class Meta:
        model = ProgrammaticEvaluationAbstract
        fields = [
            'status',
            'comment',
            'presentation',
            'category',
            'subcategory'
        ]


class AbstractReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserLightSerializer()
    abstract = AbstractAnonymSerializer(read_only=True)
    presentation = PresentationSerializer()
    status = StatusSerializer()

    class Meta:
        model = AbstractReviewer
        fields = '__all__'


class ClinicCaseAbstractReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserLightSerializer()
    clinicCase = ClinicCaseAbstractAnonymSerializer(read_only=True)
    presentation = PresentationSerializer()
    status = StatusSerializer()

    class Meta:
        model = ClinicCaseAbstractReviewer
        fields = '__all__'


class ProgrammaticEvaluationAbstractReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserLightSerializer()
    programmaticEvaluation = ProgrammaticEvaluationAbstractAnonymSerializer(read_only=True)
    presentation = PresentationSerializer()
    status = StatusSerializer()

    class Meta:
        model = ProgrammaticEvaluationAbstractReviewer
        fields = '__all__'


class AuthorAbstractReviewerSerializer(serializers.ModelSerializer):
    presentation = PresentationSerializer()
    status = StatusSerializer()

    class Meta:
        model = AbstractReviewer
        exclude = ['reviewer', 'abstract']


class AuthorClinicCaseAbstractReviewerSerializer(serializers.ModelSerializer):
    presentation = PresentationSerializer()
    status = StatusSerializer()

    class Meta:
        model = ClinicCaseAbstractReviewer
        exclude = ['reviewer', 'clinicCase']


class AuthorProgrammaticEvaluationReviewerSerializer(serializers.ModelSerializer):
    presentation = PresentationSerializer()
    status = StatusSerializer()

    class Meta:
        model = ProgrammaticEvaluationAbstractReviewer
        exclude = ['reviewer', 'programmaticEvaluation']


class SecretaryAbstractReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserLightSerializer(read_only=True)
    status = StatusSerializer()

    class Meta:
        model = AbstractReviewer
        exclude = ['abstract']


class SecretaryClinicCaseAbstractReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserLightSerializer(read_only=True)
    status = StatusSerializer()

    class Meta:
        model = ClinicCaseAbstractReviewer
        exclude = ['clinicCase']


class SecretaryProgrammaticEvaluationAbstractReviewerSerializer(serializers.ModelSerializer):
    reviewer = UserLightSerializer(read_only=True)
    status = StatusSerializer()

    class Meta:
        model = ProgrammaticEvaluationAbstractReviewer
        exclude = ['programmaticEvaluation']


class AbstractReviewerAddSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    abstract = serializers.PrimaryKeyRelatedField(queryset=Abstract.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = AbstractReviewer
        fields = '__all__'


class ClinicCaseAbstractReviewerAddSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    clinicCase = serializers.PrimaryKeyRelatedField(queryset=ClinicCaseAbstract.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = ClinicCaseAbstractReviewer
        fields = '__all__'


class ProgrammaticEvaluationAbstractReviewerAddSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    programmaticEvaluation = serializers.PrimaryKeyRelatedField(queryset=ProgrammaticEvaluationAbstract.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = ProgrammaticEvaluationAbstractReviewer
        fields = '__all__'


class AbstractReviewerUpdateSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    abstract = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = AbstractReviewer
        fields = '__all__'


class ClinicCaseAbstractReviewerUpdateSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    clinicCase = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = ClinicCaseAbstractReviewer
        fields = '__all__'


class ProgrammaticEvaluationAbstractReviewerUpdateSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    programmaticEvaluation = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = ProgrammaticEvaluationAbstractReviewer
        fields = '__all__'
