class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.characters = []
        self.current_character = None