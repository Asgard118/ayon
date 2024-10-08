import copy
import inspect
import importlib.util
import sys
import logging
import time
from pathlib import Path

from colorama import Fore, Style, init as _clrm_init
from .config import WORKDIR, TEMPDIR
import requests
import os


_clrm_init(autoreset=True)


# check dicts is match
def compare_dicts(dict1, dict2, ignore_keys=None):
    return dict1 == dict2

    if ignore_keys is None:
        ignore_keys = []

    for key, value in dict1.items():
        if key in ignore_keys:
            continue
        if key not in dict2:
            logging.debug(f"Key '{key}' not found in second dictionary")
            return False
        if isinstance(value, dict):
            if not isinstance(dict2[key], dict):
                logging.debug(
                    f"Value for key '{key}' is a dictionary in the first but not in the second"
                )
                return False
            if not compare_dicts(value, dict2[key], ignore_keys):
                logging.debug(
                    f"Values for key '{key}' in both dictionaries are not equal"
                )
                return False
        elif isinstance(value, list):
            if not isinstance(dict2[key], list):
                logging.debug(
                    f"Value for key '{key}' is a list in the first but not in the second"
                )
                return False
            if not value:
                continue
            item_types = set([type(i) for i in value])
            if len(item_types) > 1:
                logging.warning("Skip multi typed list!")
                continue
            item_type = item_types.pop()
            if item_type is dict:
                for d1 in value:
                    if not any(
                        compare_dicts(d1, d2, ignore_keys=ignore_keys)
                        for d2 in dict2[key]
                    ):
                        logging.debug(f"Dict in key {key}: not found in second dict")
                        return False
            else:
                if value != dict2[key]:
                    logging.debug(
                        f"Values for key '{key}' in both dictionaries are not equal"
                    )
                    return False
        else:
            if dict2[key] != value:
                return False
    return True


# merge dicts
def merge_dicts(d1, d2, skip_keys=None):
    if skip_keys is None:
        skip_keys = []

    result = copy.deepcopy(d2)

    for key, value in d1.items():
        if key in skip_keys:
            continue

        if key not in result:
            result[key] = value
        else:
            if isinstance(value, dict):
                if not isinstance(result[key], dict):
                    result[key] = {}
                result[key] = merge_dicts(value, result[key], skip_keys)
            elif isinstance(value, list):
                if not isinstance(result[key], list):
                    result[key] = []
                for item in value:
                    if item not in result[key]:
                        result[key].append(item)
            else:
                result[key] = value

    return result


def import_module_from_string(module_code, module_name):
    module_spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(module_spec)
    code = compile(module_code, "<string>", "exec")
    exec(code, module.__dict__)
    sys.modules[module_name] = module
    return module


def import_subclasses_from_string_module(module_code, module_name, parent_class):
    module = import_module_from_string(module_code, module_name)
    yield from get_subclass_from_module(module, parent_class=parent_class)


def get_subclass_from_module(module, parent_class):
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isclass(obj) and issubclass(obj, parent_class):
            yield obj


def import_module_from_dotted_path(import_path):
    module = importlib.import_module(import_path)
    return module


def import_module_from_path(path):
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_subclasses_from_path_module(path, parent_class):
    module = import_module_from_path(path)
    for name in dir(module):
        obj = getattr(module, name)
        if (
            inspect.isclass(obj)
            and issubclass(obj, parent_class)
            and obj is not parent_class
        ):
            yield obj


def show_dict_diffs(dict1, dict2):
    from deepdiff import DeepDiff

    diff = DeepDiff(dict1, dict2)
    if diff:
        print()
        print("diffs:", " ".join(diff.keys()))
        if "dictionary_item_added" in diff:
            print(f"{Fore.YELLOW}Missing fields:{Style.RESET_ALL}")
            for item in diff["dictionary_item_added"]:
                print(f"  {Fore.GREEN}{item}{Style.RESET_ALL}")

        if "dictionary_item_removed" in diff:
            print(f"{Fore.YELLOW}Extra field:{Style.RESET_ALL}")
            for item in diff["dictionary_item_removed"]:
                print(f"  {Fore.RED}{item}{Style.RESET_ALL}")
        if "type_changes" in diff:
            print(f"{Fore.YELLOW}Type changed: {Style.RESET_ALL}")
            for path, item in diff["type_changes"].items():
                print(
                    f"  {path}: {Fore.GREEN}{item['old_value']}({item['old_type']}) -> {Fore.RED}{item['new_value']}({item['new_type']}){Style.RESET_ALL}"
                )
        if "values_changed" in diff:
            print(f"{Fore.YELLOW}Changed values:{Style.RESET_ALL}")
            for path, item in diff["values_changed"].items():
                print(
                    f" {path}  {Fore.GREEN}{item['old_value']} -> {Fore.RED}{item['new_value']}{Style.RESET_ALL}"
                )
        if "iterable_item_removed" in diff:
            print(f"{Fore.YELLOW}Missing items:{Style.RESET_ALL}")
            for path, item in diff["iterable_item_removed"].items():
                print(f"  {Fore.RED}{path}: {item}{Style.RESET_ALL}")

        if "iterable_item_added" in diff:
            print(f"{Fore.YELLOW}Extra items:{Style.RESET_ALL}")
            for path, item in diff["iterable_item_added"].items():
                print(f"  {Fore.RED}{path}: {item}{Style.RESET_ALL}")

        print()


def download_file(url, save_file_name, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return save_file_name
        except (
            requests.exceptions.RequestException,
            requests.exceptions.ChunkedEncodingError,
        ) as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise


def download_file_to_temp(url: str):
    return download_file(url, TEMPDIR / Path(url).name)


def get_json_file_content_by_url(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
