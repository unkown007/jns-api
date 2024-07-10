from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .serializers import (
    StatusSerializer,
    KeyWordSerializer,
    PresentationSerializer,
    CoAuthorSerializer,
    AbstractSerializer,
    AbstractAddSerializer,
    AbstractStatusSerializer,
    AbstractReviewerSerializer,
    AbstractReviewerAddSerializer,
    AbstractReviewerUpdateSerializer,
    AuthorAbstractReviewerSerializer,
    SecretaryAbstractReviewerSerializer,
    ClinicCaseAbstractSerializer,
    ClinicCaseAbstractAddSerializer,
    ProgrammaticEvaluationAbstractAddSerializer,
    ProgrammaticEvaluationAbstractSerializer,
    AuthorClinicCaseAbstractReviewerSerializer,
    AuthorProgrammaticEvaluationReviewerSerializer,
    ClinicCaseAbstractStatusSerializer, ClinicCaseAbstractReviewerSerializer, ClinicCaseAbstractReviewerAddSerializer,
    SecretaryClinicCaseAbstractReviewerSerializer, ProgrammaticEvaluationAbstractStatusSerializer,
    ProgrammaticEvaluationAbstractReviewerSerializer, ProgrammaticEvaluationAbstractReviewerAddSerializer,
    SecretaryProgrammaticEvaluationAbstractReviewerSerializer, ClinicCaseAbstractReviewerUpdateSerializer,
    ProgrammaticEvaluationAbstractReviewerUpdateSerializer
)
from .models import (
    Status,
    KeyWord,
    Presentation,
    CoAuthor,
    Abstract,
    AbstractReviewer,
    ClinicCaseAbstract,
    ClinicCaseAbstractReviewer,
    ProgrammaticEvaluationAbstract,
    ProgrammaticEvaluationAbstractReviewer
)


class StatusView(APIView):
    @staticmethod
    def post(request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            stat = serializer.save()
            serializer = StatusSerializer(stat, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        states = Status.objects.all()
        serializer = StatusSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeywordView(APIView):
    @staticmethod
    def post(request):
        serializer = KeyWordSerializer(data=request.data)
        if serializer.is_valid():
            keyword = serializer.save()
            serializer = KeyWordSerializer(keyword, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        keywords = KeyWord.objects.all()
        serializer = KeyWordSerializer(keywords, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PresentationView(APIView):
    @staticmethod
    def post(request):
        serializer = PresentationSerializer(data=request.data)
        if serializer.is_valid():
            presentation = serializer.save()
            serializer = PresentationSerializer(presentation, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        presentations = Presentation.objects.all()
        serializer = PresentationSerializer(presentations, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CoAuthorView(APIView):
    @staticmethod
    def post(request):
        serializer = CoAuthorSerializer(data=request.data)
        if serializer.is_valid():
            coauthor = serializer.save()
            serializer = CoAuthorSerializer(coauthor, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        coauthors = CoAuthor.objects.all()
        serializer = CoAuthorSerializer(coauthors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractView(APIView):
    @staticmethod
    def post(request):
        serializer = AbstractAddSerializer(data=request.data)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = AbstractSerializer(abstract, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        if request.GET.get("status"):
            abstract = Abstract.objects.filter(status=request.GET.get("status"))
            serializer = AbstractSerializer(abstract, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        abstract = Abstract.objects.all()
        serializer = AbstractSerializer(abstract, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClinicalCaseView(APIView):
    @staticmethod
    def post(request):
        serializer = ClinicCaseAbstractAddSerializer(data=request.data)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = ClinicCaseAbstractSerializer(abstract, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        if request.GET.get("status"):
            abstract = ClinicCaseAbstract.objects.filter(status=request.GET.get("status"))
            serializer = ClinicCaseAbstractSerializer(abstract, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        abstract = ClinicCaseAbstract.objects.all()
        serializer = ClinicCaseAbstractSerializer(abstract, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgrammaticEvaluationView(APIView):
    @staticmethod
    def post(request):
        serializer = ProgrammaticEvaluationAbstractAddSerializer(data=request.data)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        if request.GET.get("status"):
            abstract = ProgrammaticEvaluationAbstract.objects.filter(status=request.GET.get("status"))
            serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        abstract = ProgrammaticEvaluationAbstract.objects.all()
        serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractDetailsView(APIView):
    @staticmethod
    def get(request, pk):
        abstract = Abstract.objects.filter(id=pk).first()

        if abstract is not None:
            serializer = AbstractSerializer(abstract, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        abstract = Abstract.objects.filter(id=pk).first()

        if abstract is None:
            return Response({"message": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AbstractAddSerializer(abstract, data=request.data)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = AbstractSerializer(abstract, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        abstract = Abstract.objects.filter(id=pk).first()

        if abstract is None:
            return Response({"message": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract.delete()
        return Response({"msg": "Abstract deleted successfully"}, status=status.HTTP_200_OK)


class ClinicalCaseDetailsView(APIView):

    @staticmethod
    def get(request, pk):
        abstract = ClinicCaseAbstract.objects.filter(id=pk).first()

        if abstract is not None:
            serializer = ClinicCaseAbstractSerializer(abstract, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        abstract = ClinicCaseAbstract.objects.filter(id=pk).first()

        if abstract is None:
            return Response({"message": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClinicCaseAbstractAddSerializer(abstract, data=request.data)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = ClinicCaseAbstractSerializer(abstract, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        abstract = ClinicCaseAbstract.objects.filter(id=pk).first()

        if abstract is None:
            return Response({"message": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract.delete()
        return Response({"msg": "Abstract deleted successfully"}, status=status.HTTP_200_OK)


class ProgrammaticEvaluationDetailsView(APIView):
    @staticmethod
    def get(request, pk):
        abstract = ProgrammaticEvaluationAbstract.objects.filter(id=pk).first()

        if abstract is not None:
            serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        abstract = ProgrammaticEvaluationAbstract.objects.filter(id=pk).first()

        if abstract is None:
            return Response({"message": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProgrammaticEvaluationAbstractAddSerializer(abstract, data=request.data)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        abstract = ProgrammaticEvaluationAbstract.objects.filter(id=pk).first()

        if abstract is None:
            return Response({"message": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract.delete()
        return Response({"msg": "Abstract deleted successfully"}, status=status.HTTP_200_OK)



class AuthorResumeView(APIView):
    @staticmethod
    def get(request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract_reviewer = AbstractReviewer.objects.filter(reviewer=user)
        serializer = AbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorClinicalCaseResumeView(APIView):

    @staticmethod
    def get(request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(reviewer=user)
        serializer = ClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorProgrammaticEvaluationResumeView(APIView):

    @staticmethod
    def get(request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(reviewer=user)
        serializer = ProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorAbstractReviewerView(APIView):
    @staticmethod
    def get(request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstracts = Abstract.objects.filter(author=user)
        if not abstracts.exists():
            return Response({"message": "Any Resume found for this user"}, status=status.HTTP_400_BAD_REQUEST)

        data = []
        for abstract in abstracts:
            abstract_reviewer = AbstractReviewer.objects.filter(abstract=abstract)
            serializer = AuthorAbstractReviewerSerializer(abstract_reviewer, many=True)

            abstract_serializer = AbstractSerializer(abstract, many=False)
            aux = abstract_serializer.data
            aux['reviews'] = serializer.data
            data.append(aux)

        return Response(data, status=status.HTTP_200_OK)


class AuthorClinicalCaseReviewerView(APIView):
    @staticmethod
    def get(request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstracts = ClinicCaseAbstract.objects.filter(author=user)
        if not abstracts.exists():
            return Response({"message": "Any Resume found for this user"}, status=status.HTTP_400_BAD_REQUEST)

        data = []
        for abstract in abstracts:
            abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(clinicCase=abstract)
            serializer = AuthorClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

            abstract_serializer = ClinicCaseAbstractSerializer(abstract, many=False)
            aux = abstract_serializer.data
            aux['reviews'] = serializer.data
            data.append(aux)

        return Response(data, status=status.HTTP_200_OK)


class AuthorProgrammaticEvaluationReviewerView(APIView):
    @staticmethod
    def get(request, pk):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstracts = ProgrammaticEvaluationAbstract.objects.filter(author=user)
        if not abstracts.exists():
            return Response({"message": "Any Resume found for this user"}, status=status.HTTP_400_BAD_REQUEST)

        data = []
        for abstract in abstracts:
            abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=abstract)
            serializer = AuthorProgrammaticEvaluationReviewerSerializer(abstract_reviewer, many=True)

            abstract_serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
            aux = abstract_serializer.data
            aux['reviews'] = serializer.data
            data.append(aux)

        return Response(data, status=status.HTTP_200_OK)


class SecretaryResumeView(APIView):
    @staticmethod
    def get(request):
        data = []
        if request.GET.get('abstract_status'):
            abstracts = Abstract.objects.filter(status_id=request.GET.get('abstract_status'))
            for abstract in abstracts:
                abstract_reviewer = AbstractReviewer.objects.filter(abstract=abstract)
                serializer = SecretaryAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = AbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)
        elif request.GET.get('reviewer_status'):
            abstract_ids = AbstractReviewer.objects.filter(
                status_id=request.GET.get('reviewer_status')
            ).values_list('abstract', flat=True)
            abstracts = Abstract.objects.filter(id__in=abstract_ids)
            for abstract in abstracts:
                abstract_reviewer = AbstractReviewer.objects.filter(
                    abstract=abstract,
                    status_id=request.GET.get('reviewer_status')
                )
                serializer = SecretaryAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = AbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)
        elif request.GET.get('reviewed'):
            if int(request.GET.get('reviewed')) == 1:
                abstract_ids = AbstractReviewer.objects.filter(
                    status_id__in=[5, 6, 7]
                ).values_list('abstract', flat=True)

                abstracts = Abstract.objects.filter(id__in=list(set(abstract_ids)))
                for abstract in abstracts:
                    abstract_reviewer = AbstractReviewer.objects.filter(
                        abstract=abstract
                    ).prefetch_related(
                        'abstract',
                        'reviewer'
                    )
                    serializer = SecretaryAbstractReviewerSerializer(abstract_reviewer, many=True)

                    abstract_serializer = AbstractSerializer(abstract, many=False)
                    aux = abstract_serializer.data
                    aux['reviews'] = serializer.data
                    data.append(aux)

                return Response(data, status.HTTP_200_OK)
            else:
                abstract_ids = AbstractReviewer.objects.filter(
                    status_id__in=[5, 6, 7]
                ).values_list('abstract', flat=True)

                abstracts = Abstract.objects.filter(status_id=4).exclude(id__in=list(set(abstract_ids)))
                for abstract in abstracts:
                    abstract_reviewer = AbstractReviewer.objects.filter(
                        abstract=abstract
                    )
                    serializer = SecretaryAbstractReviewerSerializer(abstract_reviewer, many=True)

                    abstract_serializer = AbstractSerializer(abstract, many=False)
                    aux = abstract_serializer.data
                    aux['reviews'] = serializer.data
                    data.append(aux)

                return Response(data, status.HTTP_200_OK)
        else:
            abstracts = Abstract.objects.all()
            for abstract in abstracts:
                abstract_reviewer = AbstractReviewer.objects.filter(abstract=abstract)
                serializer = SecretaryAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = AbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)


class SecretaryClinicalCaseView(APIView):

    @staticmethod
    def get(request):
        data = []
        if request.GET.get('abstract_status'):
            abstracts = ClinicCaseAbstract.objects.filter(status_id=request.GET.get('abstract_status'))
            for abstract in abstracts:
                abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(clinicCase=abstract)
                serializer = SecretaryClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = ClinicCaseAbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)
        elif request.GET.get('reviewer_status'):
            abstract_ids = ClinicCaseAbstractReviewer.objects.filter(
                status_id=request.GET.get('reviewer_status')
            ).values_list('clinicCase', flat=True)
            abstracts = ClinicCaseAbstract.objects.filter(id__in=abstract_ids)
            for abstract in abstracts:
                abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(
                    clinicCase=abstract,
                    status_id=request.GET.get('reviewer_status')
                )
                serializer = SecretaryClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = ClinicCaseAbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)
        elif request.GET.get('reviewed'):
            if int(request.GET.get('reviewed')) == 1:
                status_ids = Status.objects.filter(
                    name__in=[
                        "Reprovado",
                        "Aprovado - Com modificações ligeiras",
                        "Aprovado - Sem modificações"
                    ]
                ).values_list("id", flat=True)
                abstract_ids = ClinicCaseAbstractReviewer.objects.filter(
                    status_id__in=status_ids # [5, 6, 7]
                ).values_list('clinicCase', flat=True)

                abstracts = ClinicCaseAbstract.objects.filter(id__in=list(set(abstract_ids)))
                for abstract in abstracts:
                    abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(
                        clinicCase=abstract
                    )
                    serializer = SecretaryClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

                    abstract_serializer = ClinicCaseAbstractSerializer(abstract, many=False)
                    aux = abstract_serializer.data
                    aux['reviews'] = serializer.data
                    data.append(aux)

                return Response(data, status.HTTP_200_OK)
            else:
                status_ids = Status.objects.filter(
                    name__in=[
                        "Reprovado",
                        "Aprovado - Com modificações ligeiras",
                        "Aprovado - Sem modificações"
                    ]
                ).values_list("id", flat=True)
                abstract_ids = ClinicCaseAbstractReviewer.objects.filter(
                    status_id__in=status_ids # [5, 6, 7]
                ).values_list('clinicCase', flat=True)

                abstracts = ClinicCaseAbstract.objects.filter(status_id=4).exclude(id__in=list(set(abstract_ids)))
                for abstract in abstracts:
                    abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(
                        clinicCase=abstract
                    )
                    serializer = SecretaryClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

                    abstract_serializer = ClinicCaseAbstractSerializer(abstract, many=False)
                    aux = abstract_serializer.data
                    aux['reviews'] = serializer.data
                    data.append(aux)

                return Response(data, status.HTTP_200_OK)
        else:
            abstracts = ClinicCaseAbstract.objects.all()
            for abstract in abstracts:
                abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(clinicCase=abstract)
                serializer = SecretaryClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = ClinicCaseAbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)


class SecretaryProgrammaticEvaluationView(APIView):

    @staticmethod
    def get(request):
        data = []
        if request.GET.get('abstract_status'):
            abstracts = ProgrammaticEvaluationAbstract.objects.filter(status_id=request.GET.get('abstract_status'))
            for abstract in abstracts:
                abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=abstract)
                serializer = SecretaryProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)
        elif request.GET.get('reviewer_status'):
            abstract_ids = ProgrammaticEvaluationAbstractReviewer.objects.filter(
                status_id=request.GET.get('reviewer_status')
            ).values_list('programmaticEvaluation', flat=True)
            abstracts = ProgrammaticEvaluationAbstract.objects.filter(id__in=abstract_ids)
            for abstract in abstracts:
                abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(
                    programmaticEvaluation=abstract,
                    status_id=request.GET.get('reviewer_status')
                )
                serializer = SecretaryProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)
        elif request.GET.get('reviewed'):
            if int(request.GET.get('reviewed')) == 1:
                status_ids = Status.objects.filter(
                    name__in=[
                        "Reprovado",
                        "Aprovado - Com modificações ligeiras",
                        "Aprovado - Sem modificações"
                    ]
                ).values_list("id", flat=True)
                abstract_ids = ProgrammaticEvaluationAbstractReviewer.objects.filter(
                    status_id__in=status_ids  # [5, 6, 7]
                ).values_list('programmaticEvaluation', flat=True)

                abstracts = ProgrammaticEvaluationAbstract.objects.filter(id__in=list(set(abstract_ids)))
                for abstract in abstracts:
                    abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(
                        programmaticEvaluation=abstract
                    )
                    serializer = SecretaryProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

                    abstract_serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
                    aux = abstract_serializer.data
                    aux['reviews'] = serializer.data
                    data.append(aux)

                return Response(data, status.HTTP_200_OK)
            else:
                status_ids = Status.objects.filter(
                    name__in=[
                        "Reprovado",
                        "Aprovado - Com modificações ligeiras",
                        "Aprovado - Sem modificações"
                    ]
                ).values_list("id", flat=True)
                abstract_ids = ProgrammaticEvaluationAbstractReviewer.objects.filter(
                    status_id__in=status_ids  # [5, 6, 7]
                ).values_list('programmaticEvaluation', flat=True)

                abstracts = ProgrammaticEvaluationAbstract.objects.filter(status_id=4).exclude(id__in=list(set(abstract_ids)))
                for abstract in abstracts:
                    abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(
                        programmaticEvaluation=abstract
                    )
                    serializer = SecretaryProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

                    abstract_serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
                    aux = abstract_serializer.data
                    aux['reviews'] = serializer.data
                    data.append(aux)

                return Response(data, status.HTTP_200_OK)
        else:
            abstracts = ProgrammaticEvaluationAbstract.objects.all()
            for abstract in abstracts:
                abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=abstract)
                serializer = SecretaryProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

                abstract_serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)
                aux = abstract_serializer.data
                aux['reviews'] = serializer.data
                data.append(aux)

            return Response(data, status.HTTP_200_OK)


class AbstractStatusView(APIView):
    @staticmethod
    def put(request, pk):
        abstract = Abstract.objects.filter(id=pk).first()
        if abstract is None:
            return Response({"msg": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AbstractStatusSerializer(abstract, data=request.data, partial=True)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = AbstractSerializer(abstract, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClinicalCaseStatusView(APIView):
    @staticmethod
    def put(request, pk):
        abstract = ClinicCaseAbstract.objects.filter(id=pk).first()
        if abstract is None:
            return Response({"msg": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClinicCaseAbstractStatusSerializer(abstract, data=request.data, partial=True)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = ClinicCaseAbstractSerializer(abstract, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgrammaticEvaluationStatusView(APIView):

    @staticmethod
    def put(request, pk):
        abstract = ProgrammaticEvaluationAbstract.objects.filter(id=pk).first()
        if abstract is None:
            return Response({"msg": "Abstract not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProgrammaticEvaluationAbstractStatusSerializer(abstract, data=request.data, partial=True)
        if serializer.is_valid():
            abstract = serializer.save()
            serializer = ProgrammaticEvaluationAbstractSerializer(abstract, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbstractReviewerView(APIView):
    @staticmethod
    def get(request, pk):
        abstract_reviewer = AbstractReviewer.objects.filter(abstract=pk)
        if not abstract_reviewer.exists():
            return Response(
                {"message": "Abstract without reviewer allocated"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AbstractReviewerSerializer(abstract_reviewer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, pk):
        data = request.data
        # data['abstract'] = pk
        reviewers = []
        flag = False
        for reviewer in data.get('reviewer', []):
            flag = True
            serializer = AbstractReviewerAddSerializer(data={"reviewer": reviewer, "abstract": pk}, partial=True)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if flag:
            for reviewer in data.get('reviewer', []):
                serializer = AbstractReviewerAddSerializer(data={"reviewer": reviewer, "abstract": pk}, partial=True)
                if serializer.is_valid():
                    abstract_reviewer = serializer.save()
                    serializer = AbstractReviewerSerializer(abstract_reviewer, many=False)
                    reviewers.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            abstract = Abstract.objects.get(id=pk)
            abstract.status = Status.objects.get_or_create(name="Em Revisão")[0]
            abstract.save()
            return Response(reviewers, status=status.HTTP_201_CREATED)
        return Response({"message": "No Reviewer was specified"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        data = request.data

        abstract_reviewer = AbstractReviewer.objects.filter(abstract=pk)

        new_reviewers = data.get('reviewer', [])
        reviewers = [x.reviewer.id for x in abstract_reviewer]
        for new in new_reviewers:
            if new not in reviewers:
                serializer = AbstractReviewerAddSerializer(data={"reviewer": new, "abstract": pk}, partial=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if abstract_reviewer.exists():
            for x in abstract_reviewer:
                if x.reviewer.id not in new_reviewers:
                    x.delete()

        abstract_reviewer = AbstractReviewer.objects.filter(abstract=pk)
        serializer = AbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractReviewerRelocateView(APIView):

    @staticmethod
    def put(request, pk):
        data = request.data

        abstract_reviewer = AbstractReviewer.objects.filter(abstract=pk)

        new_reviewers = data.get('reviewer', [])
        reviewers = [x.reviewer.id for x in abstract_reviewer]
        for new in new_reviewers:
            if new not in reviewers:
                serializer = AbstractReviewerAddSerializer(data={"reviewer": new, "abstract": pk}, partial=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if abstract_reviewer.exists():
            for x in abstract_reviewer:
                if x.reviewer.id not in new_reviewers:
                    x.delete()

        abstract_reviewer = AbstractReviewer.objects.filter(abstract=pk)
        serializer = AbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ClinicalCaseReviewView(APIView):

    @staticmethod
    def get(request, pk):
        abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(clinicCase=pk)
        if not abstract_reviewer.exists():
            return Response(
                {"message": "Abstract without reviewer allocated"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, pk):
        data = request.data
        reviewers = []
        flag = False
        for reviewer in data.get('reviewer', []):
            flag = True
            serializer = ClinicCaseAbstractReviewerAddSerializer(data={"reviewer": reviewer, "clinicCase": pk}, partial=True)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if flag:
            for reviewer in data.get('reviewer', []):
                serializer = ClinicCaseAbstractReviewerAddSerializer(data={"reviewer": reviewer, "clinicCase": pk}, partial=True)
                if serializer.is_valid():
                    abstract_reviewer = serializer.save()
                    serializer = ClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=False)
                    reviewers.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            abstract = ClinicCaseAbstract.objects.get(id=pk)
            abstract.status = Status.objects.get_or_create(name="Em Revisão")[0]
            abstract.save()
            return Response(reviewers, status=status.HTTP_201_CREATED)
        return Response({"message": "No Reviewer was specified"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        data = request.data

        abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(clinicCase=pk)

        new_reviewers = data.get('reviewer', [])
        reviewers = [x.reviewer.id for x in abstract_reviewer]
        for new in new_reviewers:
            if new not in reviewers:
                serializer = ClinicCaseAbstractReviewerAddSerializer(data={"reviewer": new, "clinicCase": pk}, partial=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if abstract_reviewer.exists():
            for x in abstract_reviewer:
                if x.reviewer.id not in new_reviewers:
                    x.delete()

        abstract_reviewer = ClinicCaseAbstractReviewer.objects.filter(clinicCase=pk)
        serializer = ClinicCaseAbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgrammaticEvaluationReviewView(APIView):

    @staticmethod
    def get(request, pk):
        abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=pk)
        if not abstract_reviewer.exists():
            return Response(
                {"message": "Abstract without reviewer allocated"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, pk):
        data = request.data
        reviewers = []
        flag = False
        for reviewer in data.get('reviewer', []):
            flag = True
            serializer = ProgrammaticEvaluationAbstractReviewerAddSerializer(
                data={
                    "reviewer": reviewer,
                    "programmaticEvaluation": pk
                },
                partial=True
            )

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if flag:
            for reviewer in data.get('reviewer', []):
                serializer = ProgrammaticEvaluationAbstractReviewerAddSerializer(
                    data={
                        "reviewer": reviewer,
                        "programmaticEvaluation": pk
                    },
                    partial=True
                )
                if serializer.is_valid():
                    abstract_reviewer = serializer.save()
                    serializer = ProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=False)
                    reviewers.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            abstract = ProgrammaticEvaluationAbstract.objects.get(id=pk)
            abstract.status = Status.objects.get_or_create(name="Em Revisão")[0]
            abstract.save()
            return Response(reviewers, status=status.HTTP_201_CREATED)
        return Response({"message": "No Reviewer was specified"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        data = request.data

        abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=pk)

        new_reviewers = data.get('reviewer', [])
        reviewers = [x.reviewer.id for x in abstract_reviewer]
        for new in new_reviewers:
            if new not in reviewers:
                serializer = ProgrammaticEvaluationAbstractReviewerAddSerializer(data={"reviewer": new, "programmaticEvaluation": pk},
                                                                     partial=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if abstract_reviewer.exists():
            for x in abstract_reviewer:
                if x.reviewer.id not in new_reviewers:
                    x.delete()

        abstract_reviewer = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=pk)
        serializer = ProgrammaticEvaluationAbstractReviewerSerializer(abstract_reviewer, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractReviewView(APIView):
    @staticmethod
    def get(request):
        abstract_review = AbstractReviewer.objects.all()

        serializer = AbstractReviewerSerializer(abstract_review, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractCommentView(APIView):
    @staticmethod
    def put(request, pk, abstract_review):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract_review = AbstractReviewer.objects.filter(abstract=abstract_review, reviewer=pk).first()
        if abstract_review is None:
            return Response(
                {"message": "Resume not allocated to this reviewer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AbstractReviewerUpdateSerializer(abstract_review, data=request.data, partial=True)
        if serializer.is_valid():
            abstract_review = serializer.save()
            serializer = AbstractReviewerSerializer(abstract_review, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClinicalCommentView(APIView):

    @staticmethod
    def put(request, pk, abstract_review):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract_review = ClinicCaseAbstractReviewer.objects.filter(clinicCase=abstract_review, reviewer=pk).first()
        if abstract_review is None:
            return Response(
                {"message": "Resume not allocated to this reviewer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ClinicCaseAbstractReviewerUpdateSerializer(abstract_review, data=request.data, partial=True)
        if serializer.is_valid():
            abstract_review = serializer.save()
            serializer = ClinicCaseAbstractReviewerSerializer(abstract_review, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgrammaticEvaluationCommentView(APIView):

    @staticmethod
    def put(request, pk, abstract_review):
        user = User.objects.filter(id=pk).first()
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        abstract_review = ProgrammaticEvaluationAbstractReviewer.objects.filter(programmaticEvaluation=abstract_review, reviewer=pk).first()
        if abstract_review is None:
            return Response(
                {"message": "Resume not allocated to this reviewer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProgrammaticEvaluationAbstractReviewerUpdateSerializer(abstract_review, data=request.data, partial=True)
        if serializer.is_valid():
            abstract_review = serializer.save()
            serializer = ProgrammaticEvaluationAbstractReviewerSerializer(abstract_review, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
