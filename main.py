import pygame

import asyncio

import pygame

from Steuerung import Steuerung


async def main():
    pygame.init()
    steuerung = Steuerung(start_loop=False)
    await steuerung.loop()
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
