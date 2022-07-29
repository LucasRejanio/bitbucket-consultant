import os
import json
import requests
import logging

from settings import config
from services.file_manipulation import file_actions
from connector.mongo_client import MongoDBConn
from models.tokens_model import TokensModel


class RepositoryModel:
    def __init__(self, workspace, token, pages):
        self.workspace = workspace
        self.token = token
        self.pages = pages

    def get_all_repositories_from_bitbucket_api(self):
        logging.info("Method get_all_repositories_from_bitbucket_api called.")

        file_actions("delete", f"data/{self.workspace}-repositories_raw.json")

        repositories = []
        for page in range(self.pages + 1):
            if page != 0:
                logging.info("[HTTPS] Getting information about repositories...")

                url = f"https://api.bitbucket.org/2.0/repositories/"\
                        f"{self.workspace}?page={page}&pagelen=100"
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json"
                }
                response = requests.request("GET", url, headers=headers)

                if response.status_code != 200:
                    logging.error(response.json()["error"]["message"])
                    break
                else:
                    logging.info(f"[HTTPS] No problem with the request. Status code:({response.status_code})")
                    if response.json()["values"]:
                        repositories.append(response.json())

        file_actions("create", f"data/{self.workspace}-repositories_raw.json", repositories)
    
    def get_repository_names_and_language(self):
        logging.info("Function create_repositories_with_repository_names_and_language called.")

        current_repositories = []
        name_current_repositories = []

        if os.path.exists(f"data/{self.workspace}-repositories.json"):
            current_repositories = file_actions("open", f"data/{self.workspace}-repositories.json")

            for i, name in enumerate(current_repositories):
                name_current_repositories.append(name["name"])

        repositories = current_repositories

        repositories_raw = file_actions("open", f"data/{self.workspace}-repositories_raw.json")
        for i in range(len(repositories_raw)):
            for attr in repositories_raw[i]["values"]:
                slug = attr["slug"]
                if slug in name_current_repositories:
                    pass
                else:
                    logging.info(f"Repository {slug} not checked. Getting name and language...")
                    if attr["language"] != "":
                        repositories.append({"name": attr["slug"], "language": attr["language"], "pipeline": "check",
                                            "last_commit": "check", "last_commit_author": "check", "migrated": False})
                    else:
                        repositories.append({"name": attr["slug"], "language": "undefined", "pipeline": "check",
                                            "last_commit": "check", "last_commit_author": "check", "migrated": False})

        file_actions("create", f"data/{self.workspace}-repositories.json", repositories)
    
    def sync_repositories_with_workspace(self):
        if os.path.exists(f"data/{self.workspace}-repositories.json"):
            repositories_raw = file_actions("open", f"data/{self.workspace}-repositories_raw.json")
            
            repositories_in_workspace = []
            for i in range(len(repositories_raw)):
                for attr in repositories_raw[i]["values"]:
                    slug = attr["slug"] 
                    repositories_in_workspace.append(slug)
            
            current_repositories = file_actions("open", f"data/{self.workspace}-repositories.json")
            
            name_current_repositories = []
            for i, attr in enumerate(current_repositories):
                name_current_repositories.append(attr["name"])
            
            repositories_to_delete = []
            for repository in name_current_repositories:
                if repository in repositories_in_workspace:
                    pass
                else:
                    repositories_to_delete.append(repository)

            for i, attr in enumerate(current_repositories):
                for repository in repositories_to_delete:
                    if attr["name"] == repository:
                        del current_repositories[i]

            file_actions("sync", f"data/{self.workspace}-repositories.json", current_repositories)

    def check_repositories_with_pipeline(self):
        logging.info("Method check_repositories_with_pipeline called.")

        repositories = file_actions("open", f"data/{self.workspace}-repositories.json")

        for i, repository in enumerate(repositories):
            name = repository["name"]
            
            if repository["pipeline"] == "check":
                logging.info(f"[HTTPS] Checking if the {name} repository has a pipeline.")

                url = f"https://api.bitbucket.org/2.0/repositories/"\
                        f"{self.workspace}/{name}/pipelines/?size=1&page=1&pagelen=1"
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json"
                }
                response = requests.request("GET", url, headers=headers)

                if response.status_code != 200:
                    logging.error(response.json()["error"]["message"])
                    break
                else:
                    logging.info(f"[HTTPS] No problem with the request. Status code:({response.status_code})")
                    if response.json()["values"]:
                        repositories[i]["pipeline"] = True
                    else:
                        repositories[i]["pipeline"] = False

        file_actions("update", f"data/{self.workspace}-repositories.json", repositories, "pipeline")

    def get_last_commit_of_repositories(self):
        repositories = file_actions("open", f"data/{self.workspace}-repositories.json")

        for i, repository in enumerate(repositories):
            name = repository["name"]
            
            if repository["last_commit"] == "check":
                logging.info("[HTTPS] Getting the last commit "
                        f"from the {name} repository")

                url = f"https://api.bitbucket.org/2.0/repositories/"\
                        f"{self.workspace}/{name}/commits/?size=1&page=1&pagelen=1"
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json"
                }
                response = requests.request("GET", url, headers=headers)

                if response.status_code != 200:
                    logging.error(response.json()["error"]["message"])
                else:
                    logging.info(f"[HTTPS] No problem with the request. Status code:({response.status_code})")
                    try:
                        repositories[i]["last_commit"] = response.json()["values"][0]["date"][0:10]
                        repositories[i]["last_commit_author"] = response.json()["values"][0]["author"]["raw"]
                    except:
                        repositories[i]["last_commit"] = None
                        repositories[i]["last_commit_author"] = None

        file_actions("update", f"data/{self.workspace}-repositories.json", repositories, "commit")

    def write_repositories_to_the_database(self):
        repositories = file_actions("open", f"data/{self.workspace}-repositories.json")

        MongoDBConn("bitbucket").drop_collection(f"{self.workspace}-repositories")
        MongoDBConn("bitbucket").insert_many(f"{self.workspace}-repositories", repositories)


""" Function to instantiate the model """
def create_repository_model():
    logging.info("Function create_repository_model called.")
    token = TokensModel().get_access_token()

    return RepositoryModel(config.workspace, token, config.pages)
