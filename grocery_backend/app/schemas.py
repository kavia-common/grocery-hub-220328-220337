from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6), description="Password")
    name = fields.String(required=False, allow_none=True, description="Full name")


class UserLoginSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, load_only=True, description="Password")


class UserInfoSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    name = fields.Str(allow_none=True)


class ProductQuerySchema(Schema):
    search = fields.String(required=False, description="Search substring in product name/description")
    category = fields.String(required=False, description="Category filter")
    page = fields.Int(missing=1, description="Page number")
    page_size = fields.Int(missing=20, description="Page size")


class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    category = fields.Str(allow_none=True)
    price = fields.Float()
    image_url = fields.Str(allow_none=True)
    stock = fields.Int()


class CartItemCreateSchema(Schema):
    product_id = fields.Int(required=True, description="Product ID")
    quantity = fields.Int(required=True, validate=validate.Range(min=1, max=999))


class CartItemUpdateSchema(Schema):
    id = fields.Int(required=True, description="Cart item ID")
    quantity = fields.Int(required=True, validate=validate.Range(min=0, max=999), description="New quantity")


class CartItemSchema(Schema):
    id = fields.Int()
    product_id = fields.Int()
    quantity = fields.Int()
    product = fields.Nested(ProductSchema)


class OrderCreateSchema(Schema):
    address = fields.String(required=False, allow_none=True, description="Shipping address placeholder")


class OrderItemSchema(Schema):
    id = fields.Int()
    product = fields.Nested(ProductSchema)
    quantity = fields.Int()
    price = fields.Float()


class OrderSchema(Schema):
    id = fields.Int()
    total_amount = fields.Float()
    status = fields.Str()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemSchema))
