from tortoise import fields
# from datetime import datetime
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(50)
    last_name = fields.CharField(50)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(max_length=500, null=False)
    created_at = fields.DatetimeField(auto_now_add=True, description="Created datetime")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated datetime")

    def __str__(self):
        return self.username


class Notes(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(50)
    content = fields.TextField()
    user = fields.ForeignKeyField('models.User')
    created_at = fields.DatetimeField(auto_now_add=True, description="Created datetime")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated datetime")

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class SharedNoteToUser(Model):
    id = fields.IntField(pk=True)
    note = fields.ForeignKeyField('models.Notes', related_name='shared_notes')
    recipient_user = fields.ForeignKeyField('models.User', related_name='received_notes')

    def __str__(self):
        return f"Shared Note {self.note.title} to {self.recipient_user.username}"

