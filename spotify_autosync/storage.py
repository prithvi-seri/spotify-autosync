from dotenv import load_dotenv
from botocore.exceptions import ClientError
import boto3
from .config import SSM_PREFIX

load_dotenv()

ssm = boto3.client('ssm')
cache = {}

def store(field: str, value: any) -> None:
  global cache
  try:
    ssm.put_parameter(
      Name=f'{SSM_PREFIX}/{field}',
      Value=value,
      Type='SecureString' if 'token' in field else 'String',
      Overwrite=True
    )
    cache[field] = value
  except ClientError as e:
    print(f'AWS SSM Error: {e}')  

def retrieve(field: str) -> str | None:
  global cache
  if field not in cache:
    try:
      value = ssm.get_parameter(
        Name=f'{SSM_PREFIX}/{field}',
        WithDecryption=True
      )['Parameter']['Value']
      cache[field] = value
    except ClientError as e:
      error_code = e.response['Error']['Code']
      if error_code != 'ParameterNotFound': print(f'AWS SSM Error: {e}')

  return cache[field] if field in cache else None
