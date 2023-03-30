import os
import sys
from pathlib import Path

pardir = Path(__file__).absolute().parent.parent

arg1 = sys.argv[1]
with open(os.path.join(pardir, "terraform", "variables.tf"), "r+") as f:
    contents = f.read()
    new_contents = contents.replace("<gcp-project-id>", str(arg1))
    f.seek(0)
    f.write(new_contents)
    f.close()

print("Project ID has been ingested.")