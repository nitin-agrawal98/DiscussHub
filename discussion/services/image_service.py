from datetime import datetime

from config_parser.config import config
from services.s3 import s3_client


def get_file_location(author_id, ):
    return f'{author_id}/{datetime.utcnow().timestamp()}'


def upload_image(image, file_location):
    s3_client.upload_fileobj(image, config['aws']['bucket_name'], file_location,
                             ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'})
    return f'https://{config["aws"]["bucket_name"]}.s3.{config["aws"]["region"]}.amazonaws.com/{file_location}'


def delete_image(file_location):
    s3_client.delete_object(Bucket=config['aws']['bucket_name'], Key=file_location)
