class Controller:
    def __init__(self, discord_client, redis_client):
        self.discord_client = discord_client
        self.redis_client = redis_client