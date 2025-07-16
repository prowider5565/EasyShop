from tortoise import fields, models

class Order(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    items: fields.ReverseRelation["OrderItem"]

class OrderItem(models.Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField('models.Order', related_name='items')
    product_id = fields.IntField()
    quantity = fields.IntField()
