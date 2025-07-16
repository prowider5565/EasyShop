from tortoise import fields
from tortoise.models import Model


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=500)
    price = fields.IntField(max_length=50)
    owner = fields.ForeignKeyField(model_name="users.User", related_name="category")
    created_at = fields.DatetimeField(auto_now_add=True)
    category = fields.ForeignKeyField("products.Category", related_name="products")
    # category= fields.IntField(max_legth=10)
    # category = fields.ForeignKeyField('models.Category', related_name='products')
    # category = fields.ForeignKeyField("models.Category", related_name="products")

    def __str__(self):
        return self.name
