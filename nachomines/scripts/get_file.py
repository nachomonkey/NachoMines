import os
from nachomines.scripts.utils import fix_path
from pkg_resources import resource_filename

IN_NACHOMINES = os.path.abspath(".").lower().endswith("nachomines")

def get_file(filename):
    if IN_NACHOMINES:
        return fix_path("nachomines/" + filename)
    return resource_filename("nachomines", filename)
