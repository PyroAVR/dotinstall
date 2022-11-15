from sys import exit
import argparse

import asyncio

from .SubprocRunner import SubprocRunner


async def main():
    ap = argparse.ArgumentParser(prog="dotinstall")
    args, extras = ap.parse_known_args()

    loop = asyncio.get_event_loop()
    tasks = set()
    try:
        sample_task = loop.create_task(SubprocRunner("ls").run())
        tasks.add(sample_task)
        sample_task.add_done_callback(tasks.discard)

        await asyncio.gather(*tasks)

    except:
        raise


if __name__ == "__main__":
    exit(asyncio.run(main(), debug=True))
