from mongoengine import *

class LearningPath(Document):
    name = StringField(required=True)
    abilities = ListField(ReferenceField('Ability'), default=[], required=True)
    role = ReferenceField('Role', required=True)