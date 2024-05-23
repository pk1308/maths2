import os
import subprocess
import sys
from loguru import logger
from shared.functions import get_git_status_files, create_md, update_my_docs, deploy_mkdocs

logger.remove()
logger.add(sys.stdout, colorize=True, format="{time} | {level} | {message}")

if __name__ == "__main__":

    repo_path = os.getcwd()
    # subprocess.run(["bash", os.path.join(repo_path, "driver_folder", "nbcovert.sh")])
    files = get_git_status_files(repo_path)
    # logger.info(files)

    status = create_md(files_to_create=files)
    logger.info(status)
    if status:
        files = get_git_status_files(repo_path)
        update_my_docs()
        logger.info("successful update")

    else:
        logger.error("cant update ")
    logger.info("deploy mk docs ")

    deploy_mkdocs()
    logger.info("deployed mk docs ")
