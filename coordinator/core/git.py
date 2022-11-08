"""
Module for remaining up-to-date the test_process git repo and test scripts.
"""

import os
import git

from .config import config, GIT_REPO_PATH

logger = config["logger"]


def clone_repo():
    """Clone the test_process repo if it is not exists."""
    if not os.path.exists(GIT_REPO_PATH):
        logger.info("Test process repo is not exists, cloning.")
        git.Repo.clone_from(
            "https://github.com/sixfab/tinycell_test-process", GIT_REPO_PATH
        )
    else:
        logger.debug("Test process repo is already existed.")


def update_repo():
    """Update the test_process git repo if it is necessary."""
    repo = git.Repo(GIT_REPO_PATH)

    if repo.is_dirty():
        logger.info("Test process repo is dirty, pulling changes.")
        repo.git.pull()
