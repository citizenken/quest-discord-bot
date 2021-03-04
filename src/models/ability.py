from mongoengine import *

class Ability(Document):
    name = StringField(required=True, unique=True)
    # path = ReferenceField('LearningPath', required=True)
    path = StringField()
    step = IntField(required=True)
    cost = IntField(required=True)
    description = StringField(required=True)
    ability_rolls = ListField(ReferenceField('AbilityRoll'), default=[])

    def create(self, **loaded):
        self.save()
        if loaded['ability_rolls']:
            for re in loaded['ability_rolls']:
                ability_roll = AbilityRoll.objects(name=re['name'])
                import pdb; pdb.set_trace()
                if not ability_roll:
                    ability_roll = AbilityRoll(**re)
                    ability_roll.save()
                else:
                    ability_roll = ability_roll[0]

                self.ability_rolls.append(ability_roll)

            self.save()

        return response_details

class AbilityRoll(Document):
    name = StringField(required=True)
    upper = IntField(required=True)
    lower = IntField(required=True)
    description = StringField(required=True)
    dmg_multiplier = IntField()