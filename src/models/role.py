from mongoengine import *

class Role(Document):
    name = StringField(required=True)
    learning_path = ListField(ReferenceField('LearningPath'), default=[], required=True)