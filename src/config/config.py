from starlette.config import Config

config = Config(".env")


DEBUG: bool = config("DEBUG", cast=bool, default=False)
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
DEPLOYMENT_ID = config("DEPLOYMENT_ID")
EPIC_API = "https://api.epicgames.dev"
SERVERLIST_URL = "https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json"

# Discord
DEVELOPMENT_BOT_TOKEN = config("DEVELOPMENT_BOT_TOKEN")
PRODUCTION_BOT_TOKEN = config("PRODUCTION_BOT_TOKEN")