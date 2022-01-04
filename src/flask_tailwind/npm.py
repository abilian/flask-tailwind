import subprocess

from textwrap import dedent

NPM_BIN_PATH = "npm"


class NPMException(Exception):
    pass


class NPM:
    cwd: str = None
    npm_bin_path: str = None

    def __init__(self, cwd=None, npm_bin_path=None):
        self.npm_bin_path = npm_bin_path if npm_bin_path else NPM_BIN_PATH
        self.cwd = cwd

    def run(self, *args):
        try:
            subprocess.run([self.npm_bin_path] + list(args), cwd=self.cwd)
        except OSError:
            raise NPMException(dedent(
                """
                It looks like node.js and/or npm is not installed or cannot be found.
                Visit https://nodejs.org to download and install node.js for your system.
                If you have npm installed and still getting this error message,
                set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.
                
                Example:
                NPM_BIN_PATH = "/usr/local/bin/npm"
                """
            ))
