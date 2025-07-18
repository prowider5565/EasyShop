from tortoise import fields
from tortoise.models import Model

class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name