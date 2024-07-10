from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, SubCategorySerializer, SubCategoryAddSerializer
from .models import Category, SubCategory


class CategoryView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryView(APIView):

    def get(self, request):
        if request.GET.get('category'):
            subcategories = SubCategory.objects.filter(category=request.GET.get('category'))
            serializer = SubCategorySerializer(subcategories, many=True)

            return Response(serializer.data, status.HTTP_200_OK)

        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = SubCategoryAddSerializer(data=request.data)
        if serializer.is_valid():
            subcategory = serializer.save()
            serializer = SubCategorySerializer(subcategory, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    @staticmethod
    def get(request, pk):
        category = Category.objects.filter(pk=pk).first()
        if category is not None:
            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response([], status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        category = Category.objects.filter(pk=pk).first()
        if category is None:
            return Response({"message": "Category not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        category = Category.objects.filter(pk=pk).first()
        if category is not None:
            category.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({"message": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)


class SubCategorySpecView(APIView):

    def get(self, request, pk, format=None):
        subcategory = SubCategory.objects.filter(category_id=pk)

        if subcategory.exists():
            serializer = SubCategorySerializer(subcategory, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

        return Response([], status.HTTP_400_BAD_REQUEST)


class SubCategoryDetailView(APIView):
    @staticmethod
    def get(request, pk, format=None):
        subcategory = SubCategory.objects.filter(id=pk).first()

        if subcategory is not None:
            serializer = SubCategorySerializer(subcategory, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "Subcategory not found"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk, format=None):
        subcategory = SubCategory.objects.filter(id=pk).first()

        if subcategory is None:
            return Response({"message": "SubCategory not found"}, status=status.HTTP_200_OK)

        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = SubCategorySerializer(subcategory, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk, format=None):
        subcategory = SubCategory.objects.filter(id=pk).first()
        if subcategory is not None:
            subcategory.delete()
            return Response(status=status.HTTP_200_OK)

        return Response({"message": "Subcategory not found"}, status=status.HTTP_400_BAD_REQUEST)

