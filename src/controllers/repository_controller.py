import logging

from models.repository_model import create_repository_model


class RepositoryController:
    """ Constructor method """
    def __init__(self):
        self.repository_model = create_repository_model()

    def update_repositories(self):
        logging.info("Method update_repositories called.")

        self.repository_model.get_all_repositories_from_bitbucket_api()
        self.repository_model.get_repository_names_and_language()
        self.repository_model.sync_repositories_with_workspace()
        self.repository_model.check_repositories_with_pipeline()
        self.repository_model.get_last_commit_of_repositories()
        self.repository_model.write_repositories_to_the_database()

