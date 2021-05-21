from boto3 import client
import yaml
from typing import Dict



class Collector:
    def __init__(self, config: Dict):
        self.config = config
        self._credentials = None
        self._s3 = None
    
    def login(
        self,
        username: str,
        password: str
    ) -> None:
        user_pool_response = self._login_user_pool(username, password)
        id_token = user_pool_response['AuthenticationResult']['IdToken']
        self._credentials = self._acquire_credentials(id_token)
    
    def _login_user_pool(
        self,
        username: str,
        password: str
    ) -> Dict:
        cognito = client('cognito-idp', region_name=self.config['REGION'])
        user_pool_response = cognito.initiate_auth(
            ClientId=self.config['CLIENT_ID'],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            }
        )
        return user_pool_response

    def _acquire_credentials(self, id_token: str) -> Dict:
        logins = {
            f'cognito-idp.{self.config["REGION"]}.amazonaws.com/{self.config["USER_POOL_ID"]}': id_token
        }
        identity = client('cognito-identity', region_name=self.config['REGION'])
        id_response = identity.get_id(
            IdentityPoolId=self.config['IDENTITY_POOL_ID'],
            Logins=logins
        )
        cred_response = identity.get_credentials_for_identity(
            IdentityId=id_response['IdentityId'],
            Logins=logins
        )
        credentials = cred_response['Credentials']
        return credentials

    
    def upload_file(self, file_path: str) -> Dict:
        response = self.s3.upload_file(
            Filename=file_path,
            Bucket=self.config['BUCKET_NAME'],
            Key=file_path.split('/')[-1]
        )
        return response

    
    @property
    def s3(self):
        if self._s3 is None:
            self._s3 = client(
                's3',
                region_name=self.config['REGION'],
                aws_access_key_id=self._credentials['AccessKeyId'],
                aws_session_token=self._credentials['SessionToken'],
                aws_secret_access_key=self._credentials['SecretKey']
            )
        return self._s3
    

        