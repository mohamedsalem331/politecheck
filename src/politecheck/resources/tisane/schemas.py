from marshmallow import Schema, fields, validate

class SettingsSchema(Schema):
    snippets = fields.Boolean(required=True)
    explain = fields.Boolean(required=True)

class TisaneRequestSchema(Schema):
    language = fields.String(required=True, validate=validate.Length(min=2, max=2))
    content = fields.String(required=True)
    settings = fields.Nested(SettingsSchema, required=True)
    user_id = fields.String(required=True, validate=validate.Length(min=5, max=100))