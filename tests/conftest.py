import json
import os
import shutil
from pathlib import Path
import tempfile

import pytest

workdir = Path(tempfile.mkdtemp())
conf_file = workdir

@pytest.fixture(scope="session")
def workdir():
    workdir.mkdir(exist_ok=True)
    with conf_file.open("w") as f:
        json.dump({"jey": "value"}, f)

    os.environ["AYON_TOOLS_WORKDIR"] = workdir.as_posix()
    yield workdir
    shutil.rmtree(workdir)


# TODO create testing config file

# TODO main fixtures
# TODO testing studios
