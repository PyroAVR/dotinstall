import subprocess
import asyncio
from os import environ, listdir
import pathlib

class SubprocRunner(object):
    """
    Convenience class to locate a program on the PATH, and run it.
    """

    def __init__(self, *args, wrap_stdin=False, wrap_stdout=True, wrap_stderr=False):
        self.prog = args[0].strip()
        if len(args) > 1:
            self.args = args[1:]
        else:
            self.args = list()

        self.wrap_stdin = wrap_stdin
        self.wrap_stdout = wrap_stdout
        self.wrap_stderr = wrap_stderr

        try:
            search_path = environ["PATH"]
        except KeyError:
            print("PATH not found in environment. something is very wrong.")
            raise

        for path in search_path.split(":"):
            files = listdir(path)
            found = False
            if self.prog in files:
                self.prog = pathlib.Path(path).joinpath(self.prog)
                found = True
                break

        if not found:
            raise OSError(f"Requested program \"{self.prog}\" was not found on PATH")

    async def run(self, *args, **kwargs):
        task = await asyncio.create_subprocess_exec(
            self.prog, *self.args,
            stdin=None if not self.wrap_stdin else asyncio.subprocess.PIPE,
            stdout=None if not self.wrap_stdout else asyncio.subprocess.PIPE,
            stderr=None if not self.wrap_stderr else asyncio.subprocess.PIPE
        )
        stdout, _ = await task.communicate()
        stdout = stdout.decode("utf-8")
        print(stdout)

