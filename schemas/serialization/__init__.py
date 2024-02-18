from marshmallow import Schema
from marshmallow import fields


class SchemaSerializeDocJson(Schema):
  id   = fields.Int()
  data = fields.Dict()


class SchemaSerializeDocJsonTimes(SchemaSerializeDocJson):
  created_at = fields.DateTime()
  updated_at = fields.DateTime()

