import os
import subprocess
import sys
from pathlib import Path
import time

import yaml
from git import Repo
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger

from .variables import DEFAULT_PDF_URL
from .compress_file import compress_pdf

logger.remove()
logger.add(sys.stdout, colorize=True, format="{time} | {level} | {message}")


def load_pdf_from_url(url=DEFAULT_PDF_URL):
    """_summary_

    Args:
        url (_type_, optional): _description_. Defaults to DEFAULT_PDF_URL.

    Returns:
        _type_: _description_
    """
    # Your code here
    loader = PyPDFium2Loader(url)
    return loader.load()


def load_pdf_from_file(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Create an instance of PyPDFium2Loader with the file path
    loader = PyPDFium2Loader(file_path)

    # Load the PDF document using the loader
    pdf_document = loader.load()

    # Return the loaded PDF document
    return pdf_document


def get_git_status_files(repo_path_to_update):
    """
  This function takes the path to a Git repository and returns a list of files 
  with their paths based on the git status.

  Args:
      repo_path_to_update (str): Path to the Git repository.

  Returns:
      list: List of strings representing file paths.
  """

    # Open the Git repository
    repo = Repo(repo_path_to_update)

    # Initialize an empty list to store file paths
    files_to_commit = []

    # Get modified and staged files
    for item in repo.index.diff(None):
        files_to_commit.append(item.a_path)

    # Get untracked files
    files_to_commit.extend(repo.untracked_files)

    # Return the list of files
    return files_to_commit


def read_yaml_as_dict(path_to_yaml: Path):
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml, encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        raise e


def write_yaml(file_path: Path, data: dict = None):
    """ write yaml file from dict

    Args:
        file_path (Path):  file path with file name 
        data (dict, optional): Data to save as yaml

    Raises:
        App_Exception: _description_
    """

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as yaml_file:
            if data is not None:
                yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)
    except Exception as e:
        raise e


def update_my_docs(folder_path="./docs"):
    """_summary_

    Args:
        folder_path (str, optional): _description_. Defaults to "./docs".
    """
    yaml_file = read_yaml_as_dict(Path("mkdocs.yml"))
    markdown_files = []
    for root, _, files_to_check in os.walk(folder_path):
        for filename in files_to_check:
            if filename.endswith(".md"):
                full_path = os.path.join(root, filename)
                directory_name = "/".join(full_path.split("/")[2:])
                markdown_files.append(directory_name)

    nav_value = {"Home": []}
    for file in markdown_files:
        split_value = file.split("/")
        if len(split_value) == 1:
            nav_value["Home"].append(file)
        else:
            key = split_value[0]
            if key not in nav_value.keys():
                nav_value[key] = [file]
            else:
                nav_value[key].append(file)

    yaml_file['nav'] = [{key: value} for key, value in nav_value.items()]

    file_path = Path(os.path.join(os.getcwd(), "mkdocs.yml"))
    write_yaml(file_path, yaml_file)


def summarize(file_path, context_base="summarize the following text"):
    """_summary_

    Args:
        context_base:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    pages = load_pdf_from_file(file_path=file_path)

    # Setup the Google Generative AI model and invoke it using a human-friendly prompt
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(f"{context_base}: \n {pages}:")

    return result.content


def create_md(files_to_create):
    """
  This function attempts to create Markdown files with information about 
  provided PDF files.

  Args:
      files_to_create (list): List of file paths.

  Returns:
      bool: True if successful, False otherwise.
  """
    success = True
    for file_to in files_to_create:
        if file_to.endswith(".pdf"):
            new_filename = os.path.splitext(file_to)[0] + ".md"
            try:
                with open(new_filename, "w+", encoding="utf-8") as f:
                    data_to_write = summarize(file_to)
                    # compress_pdf(file_to)
                    f.write(f"# {os.path.basename(file_to)} (PDF file)\n")
                    f.write("**Summary**\n")
                    f.write(data_to_write)
                    f.write("\n")
                    f.write("**Lec file**\n")
                    f.write(f"# {os.path.basename(file_to)} (PDF file)\n")
                    path_ = os.path.basename(file_to)
                    time.sleep(60)

                    data = f"![Alt text](<./{path_}>)" + '{ type=application/pdf style="min-height:100vh;width:100%" }'
                    f.write(data)

            except Exception as e:
                logger.info(f"Error creating {new_filename}: {e}")
                success = False
        else:
            logger.info(f"{file_to} is not a PDF file.")
    return success


def deploy_mkdocs():
    """
  This function deploys the MkDocs site using mkdocs gh-deploy.

  Raises:
      CalledProcessError: If the subprocess call fails.
  """
    try:
        subprocess.run(['mkdocs', 'gh-deploy', '-f', './mkdocs.yml'], check=True)
        logger.info("MkDocs site deployed successfully!")
    except subprocess.CalledProcessError as error:
        logger.info(f"Error deploying MkDocs site: {error}")
