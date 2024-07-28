import os
import datetime

from dotenv import load_dotenv

load_dotenv()

config = {
    "services": {
        "user_service": os.getenv("USER_SERVICE"),
        "discussion_service": os.getenv("DISCUSSION_SERVICE"),
    },
    "jwt": {
            "secret_key": os.getenv("JWT_SECRET_KEY"),
            "access_token_expires": datetime.timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))),
            "refresh_token_expires": datetime.timedelta(seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES"))),
        }
}
