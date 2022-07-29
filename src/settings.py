import logging
import os
from dotenv import load_dotenv


class Settings:
    """ Contstuctor method """
    def __init__(self, environment):
        self.environment = environment
        self.workspace = None
        self.token = None
        self.pages = None

    def set_envs_for_environment(self):
        logging.info("Method set_envs_for_environment called.")

        if self.environment == "prod":
            load_dotenv()
            self.workspace = str(os.getenv("WORKSPACE"))
            self.token = str(os.getenv("TOKEN"))
            self.pages = int(os.getenv("PAGES"))
            self.sync = str(os.getenv("SYNC"))
            self.oauth_url = "https://bitbucket.org/site/oauth2/access_token"
            self.oauth_client_id = os.getenv("OAUTH_CLIENT_ID")
            self.oauth_secret = os.getenv("OAUTH_SECRET")
            self.oauth_code = os.getenv("OAUTH_CODE")

        elif self.environment == "dev":
            self.workspace = "will-bank"
            self.token = "S3UT0K3N"
            self.pages = 1
            self.sync = "True"
        else:
            print("Environment does not exist. Use 'dev' or 'prod'.")
            exit()

load_dotenv()
environment = str(os.getenv("ENVIRONMENT", "dev"))
config = Settings(environment)
config.set_envs_for_environment()
