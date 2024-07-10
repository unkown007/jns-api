from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return f'{self.name}'


class SubCategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subcategory'

    def __str__(self):
        return f'{self.name} - {self.category}'
