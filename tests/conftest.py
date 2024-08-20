import os
from pathlib import Path
import tempfile

workdir = Path(tempfile.mkdtemp())
conf_file = workdir / "lmsk_config_tests.yml"

os.environ["AYON_TOOLS_WORKDIR"] = workdir.as_posix()

# TODO create testing config file

# TODO main fixtures
# TODO testing studios
