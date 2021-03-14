from django.db import models
from django.db.models.fields import CharField, TextField

# Create your models here.
class post(models.Model):
    created_date = CharField(max_length=24)
    message = TextField()
    formatted_date = CharField(max_length=24)
    
    def __str__(self) -> str:
        return f"Date: {self.formatted_date} Message: {self.message}."