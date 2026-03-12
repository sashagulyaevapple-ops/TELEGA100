import random
import asyncio

async def delay():

    pause = random.randint(10,30)

    print(f"⏳ Антибан пауза {pause}")

    await asyncio.sleep(pause)