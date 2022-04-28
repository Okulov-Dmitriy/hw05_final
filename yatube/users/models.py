# # library/models.py
# from django.db import models
# from django.core.validators import MinValueValidator

# # Создадим модель, в которой будем хранить данные о книгах
# class Book(models.Model):
#     name = models.CharField(max_length=200)   # Название
#     isbn = models.CharField(max_length=100)   # Индекс издания
#     pages = models.IntegerField(              # Количество страниц
#         validators=[MinValueValidator(1)]
#     )
