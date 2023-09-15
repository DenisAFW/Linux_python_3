import pytest
import yaml
from test_positive import checkout
import random
import string
from datetime import datetime

with open('config.yaml', encoding='utf-8') as fy:
    data = yaml.safe_load(fy)


@pytest.fixture
def make_folders():
    return checkout(
        "mkdir {} {} {} {}".format(data["folderin"], data["folderout"], data["folderext"], data["folderbad"]), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folderin"], data["folderout"],
                                                        data["folderext"], data["folderbad"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs=1K count=1 iflag=fullblock".format(data["folderin"], filename),
                    ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    test_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folderin"], subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folderin"], subfoldername,
                                                                                      test_filename, data["bs"]), ""):
        return subfoldername, None

    return subfoldername, test_filename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat_pc():
    checkout("dd if={} bs=1K >>{}".format(data["load_pc"], data["correct_dir"]), "")
