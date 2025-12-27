import asyncio
import platform
import sys

import pygame

from Steuerung import Steuerung


def running_in_browser() -> bool:
    return sys.platform == "emscripten"


def is_wasm_cpu() -> bool:
    return "wasm" in platform.machine().lower()


async def main() -> None:
    pygame.init()
    if running_in_browser():
        pygame.display.init()

    steuerung = Steuerung()
    await steuerung.loop()
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
