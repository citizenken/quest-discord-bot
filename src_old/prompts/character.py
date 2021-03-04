class CharacterPrompts:
    character_template_prompts = {
        'name_pronouns': {
            'text': 'My name is \_\_\_\_\_, my pronouns are \_\_\_\_\_',
            'regex': 'My name is (?P<name>.+), my pronouns are (?P<pronouns>.+)',
            },
        'age_height': {
            'text': 'I\'m \_\_\_\_\_ years old and stand \_\_\_\_\_ tall.',
            'regex': 'I\'m (?P<age>\d+) years old and stand (?P<height>.+) tall.'
            },
        'role': {
            'text': 'I\'m the party\'s \_\_\_\_\_\_\_\_\_',
            'regex': 'I\'m the party\'s (?P<role>.+)',
            },
        'features': {
            'text': 'When people see me, they first notice my \_\_\_\_\_, \_\_\_\_\_, and \_\_\_\_\_',
            'regex': 'When people see me, they first notice my (?P<feature1>.*), (?P<feature2>.*), and (?P<feature3>.*)',
            },
        'clothing_movement': {
            'text': 'I wear \_\_\_\_\_, \_\_\_\_\_ and move with \_\_\_\_\_',
            'regex': 'I wear (?P<clothing1>.*), (?P<clothing2>.*) and move with (?P<movement>.*)',
            },
        'home_culture': {
            'text': 'I\'m from \_\_\_\_\_ where my people are known for \_\_\_\_\_\_\_\_\_\_',
            'regex': 'I\'m from (?P<home>.*) where my people are known for (?P<culture>.*)',
            },
        'belief_flaws': {
            'text': 'I believe in \_\_\_\_\_ but my \_\_\_\_\_ side can get in my way.',
            'regex': 'I believe in (?P<belief>.*) but my (?P<flaws>.*) side can get in my way.',
            },
        'dream': {
            'text': 'I dream of \_\_\_\_\_\_\_\_\_',
            'regex': 'I dream of (?P<dream>.*)',
            }
    }
    character_create_path = [
        {
            'property': 'name',
            'prompt': 'Let\'s make a character.\nWhat\'s your name?'
        },
        {
            'property': 'pronouns',
            'prompt': 'What\'re your pronouns?'
        },
        {
            'property': 'age',
            'prompt': 'How old are you?'
        },
        {
            'property': 'height',
            'prompt': 'How tall are you?'
        },
        {
            'property': 'role',
            'prompt': 'What role(s) do you fill in your party?'
        },
        {
            'property': 'features',
            'prompt': 'When people see you, what do they first notice?'
        },
        {
            'property': 'clothing',
            'prompt': 'What do you wear?'
        },
    ]