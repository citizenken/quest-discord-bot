class CharacterPrompts:
    character_create_prompt = """
Let's make you a character.

Copy the following text (including backticks) and fill in the form. For multiple values in a field, separate
each item with a `,`. Send it back with the command `!character create submit` to get your new character!

\`\`\`
{% for attr, prompt in creation_attrs.items() -%}
{{ prompt | safe }}:
{% endfor -%}
\`\`\`
"""
    character_list_prompt = """
You own the following characters. To get more info, use the `!character describe <character name>` command,
passing in the character name. To set a character as the current character, use the `!character current <character name>` command.
```
{% for char in list_of_characters -%}
{{ char.name }} {{ char.role }}
{% endfor -%}
```
"""