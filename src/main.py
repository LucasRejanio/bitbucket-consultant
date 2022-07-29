import logging

logging.basicConfig(format='| %(asctime)s | [%(levelname)s]:: %(message)s', level=logging.INFO)
logging.info('Admin logged in!')

from flask import Flask, request, jsonify
from services.bootstrap import create_data_dir
from controllers.repository_controller import RepositoryController

app = Flask(__name__)

@app.route("/update")
def update():
    logging.info('----------- Start Bitbucket API Consult to Update -----------')
    create_data_dir()
    RepositoryController().update_repositories()

    return jsonify({"message": "data updated"})


@app.route("/migrate")
def migrate():
    logging.info('----------- Start Bitbucket API to Migrate Repository -----------')
    # here we want to get the value of repository (i.e. ?repository=some-value)
    repository = request.args.get("repository")

    if repository:
        return jsonify({"message": f"repository {repository} has been migrated"})
    else:
        return jsonify({"message": "you need provide a repository to migrate"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
