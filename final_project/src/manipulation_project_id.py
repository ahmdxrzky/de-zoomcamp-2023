import os
import sys
from pathlib import Path

arg1 = sys.argv[1]
pardir = Path(__file__).absolute().parent.parent
files = [os.path.join(pardir, "Dockerfile"), os.path.join(pardir, "terraform", "variables.tf")]

for filename in files:
    with open(filename, "r+") as f:
        contents = f.read()
        new_contents = contents.replace("<gcp-project-id>", str(arg1))
        f.seek(0)
        f.write(new_contents)
        f.close()

print("Project ID has been ingested two those files.")