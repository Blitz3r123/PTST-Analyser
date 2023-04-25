import os
import sys
import re
import shutil

from pprint import pprint
from rich.console import Console
from rich.traceback import install
from rich.table import Table

install()
console = Console(record=True)

