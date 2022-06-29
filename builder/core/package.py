import os


class Packager:
    """builder for packager."""

    def __init__(self) -> None:
        pass

    def upload(self):
        os.system("rm -v -rf dist")
        os.system("poetry build")
        os.system("python3 -m twine upload dist/* -r nexus")
