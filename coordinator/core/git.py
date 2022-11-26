"""
Module for remaining up-to-date the test_process git repo and test scripts.
"""

import os
import subprocess

from .config import config, GIT_REPO_PATH, GIT_REPO_BRANCH, GIT_REMOTE_LINK

logger = config["logger"]


def git_shell_command(command, cwd=GIT_REPO_PATH) -> int:
    """Execute shell command."""
    try:
        com = command.split(" ")
        cp = subprocess.run(
            com,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            cwd=cwd,
        )
    except Exception as error:
        logger.error(error)
        return None
    else:
        return cp.returncode


def clone_repo() -> None:
    """Clone the test_process repo if it is not exists."""
    if not os.path.exists(GIT_REPO_PATH):
        logger.info("Test process repo is not exists, cloning.")

        result = git_shell_command(
            f"git clone {GIT_REMOTE_LINK} {GIT_REPO_PATH}", cwd="."
        )

        if result == 0:
            logger.info("Test process repo cloned.")


def switch_desired_branch() -> None:
    """Switch to desired branch"""
    result = git_shell_command(f"git checkout {GIT_REPO_BRANCH}")

    if result == 0:
        logger.info(f"Switched to {GIT_REPO_BRANCH} branch.")


def update_repo() -> None:
    """Update the test_process git repo if it is necessary."""

    result = git_shell_command("git reset --hard")
    if result == 0:
        logger.info(
            "Test process repo resetted. Uncommitted changes are discarded."
        )

    result = git_shell_command("git pull")
    if result == 0:
        logger.info("Test process repo updated.")
