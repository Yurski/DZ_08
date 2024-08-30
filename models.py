from mongoengine import Document, fields, connect
import os

# Підключення до бази даних MongoDB
connect(
    db='authors_db',
    host=os.getenv('MONGO_URI'),
    username=os.getenv('DB_ADMIN'),
    password=os.getenv('DB_PASSWORD')
)

class Author(Document):
    fullname = fields.StringField(required=True, unique=True)
    born_date = fields.StringField()
    born_location = fields.StringField()
    description = fields.StringField()

class Quote(Document):
    tags = fields.ListField(fields.StringField())
    author = fields.ReferenceField(Author)
    quote = fields.StringField()

class Contact(Document):
    fullname = fields.StringField(required=True)
    email = fields.EmailField(required=True)
    phone_number = fields.StringField()
    message_sent = fields.BooleanField(default=False)
    preferred_contact_method = fields.StringField(choices=['email', 'sms'])
