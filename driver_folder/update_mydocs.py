import os
from pathlib import Path
import yaml
import sys
from loguru import logger


logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")


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
        with open(path_to_yaml) as yaml_file:
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
        with open(file_path, "w") as yaml_file:
            if data is not None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        raise e


def update_mydocs(folder_path="./docs"):
    """_summary_

    Args:
        folder_path (str, optional): _description_. Defaults to "./docs".
    """
    yaml_file = read_yaml_as_dict(Path("mkdocs.yml"))
    markdown_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
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
                
    yaml_file['nav'] = [{key:value}for key , value in nav_value.items()]

    file_path = Path(os.path.join(os.getcwd(), "mkdocs.yml"))
    write_yaml(file_path, yaml_file)


if __name__ == "__main__":
    update_mydocs()
