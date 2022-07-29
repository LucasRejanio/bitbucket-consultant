from datetime import datetime
import requests
from services.loggers import create_logger
from settings import config
from connector.mongo_client import MongoDBConn


logger = create_logger(__name__)


class TokensModel:
    entity = MongoDBConn("bitbucket")

    def get_access_token(self) -> str:
        token = ""

        if not self.token_exists():
            logger.info("Getting first token")

            status_code, request_body = self.get_access_token_from_bitbucket(
                "authorization_code",
                config.oauth_code
            )

            if status_code == 200:
                self.save_response(request_body)

                token = self.entity.find_one("tokens")["access_token"]

        elif self.token_is_expired():
            logger.info("token expired, getting a new token")

            refresh_token = self.entity.find_one("tokens")["refresh_token"]

            status_code, request_body = self.get_access_token_from_bitbucket(
                "refresh_token", refresh_token
            )

            if status_code == 200:
                self.save_response(request_body)
                token = self.entity.find_one("tokens")["access_token"]
        else:
            token = self.entity.find_one("tokens")["access_token"]

        return token

    def get_access_token_from_bitbucket(self, grant_type, code) -> tuple[int, dict]:
        code_name = "code" if grant_type == "authorization_code" else "refresh_token"
        data = {code_name: code, "grant_type": grant_type}
        session = requests.Session()
        session.auth = (config.oauth_client_id, config.oauth_secret)
        response = session.post(url=config.oauth_url, data=data)

        logger.info(f"status code: {response.status_code}, body: {response.text}")

        return (response.status_code, response.json())

    def token_exists(self) -> bool:
        if self.entity.find_one("tokens") is None:
            return False

        return True

    def token_is_expired(self):
        now = datetime.now()
        expires_in = self.entity.find_one("tokens")["expires_in"]
        expires_in_date = datetime.fromtimestamp(expires_in)

        if expires_in_date <= now:
            return True

        return False

    def save_response(self, request_body: dict):
        request_body["expires_in"] += self.current_timestamp()

        self.fresh_tokens()

        inserted_id = self.entity.insert_one("tokens", request_body).inserted_id
        logger.info(f"Token inserted_id: {inserted_id}")

    def fresh_tokens(self):
        self.entity.drop_collection("tokens")

    def current_timestamp(self) -> float:
        now = datetime.now()

        return datetime.timestamp(now)
