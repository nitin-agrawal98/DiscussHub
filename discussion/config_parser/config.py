import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "db": {
        "username": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
        "uri": f'mysql+pymysql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@localhost/{os.getenv("DB_NAME")}',
    },
    "aws": {
        "region": os.getenv("AWS_REGION"),
        "bucket_name": os.getenv("AWS_BUCKET_NAME"),
    },
    "es": {
        "url": os.getenv("ES_URL"),
    },
}
