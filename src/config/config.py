
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")



DEBUG: bool = config("DEBUG", cast=bool, default=False)
CLIENT_ID= config("CLIENT_ID", cast=Secret)
CLIENT_SECRET= config("CLIENT_SECRET", cast=Secret)
DEPLOYMENT_ID= config("DEPLOYMENT_ID", cast=Secret)
EPIC_API = "https://api.epicgames.dev"
SERVERLIST_URL = "https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json"

# Discord
DEVELOPMENT_BOT_TOKEN = config("DEVELOPMENT_BOT_TOKEN", cast=Secret)
PRODUCTION_BOT_TOKEN = config("PRODUCTION_BOT_TOKEN", cast=Secret)