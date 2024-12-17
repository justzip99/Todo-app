from settings.configuration import Config

TORTOISE_ORM = {
    "connections": {
        "default": Config.DB_CONNECTION,
    },
    "apps": {
        "models": {
            "models": ["aerich.models", *Config.DB_MODELS],
            "default_connection": "default",
        }
    },
}
