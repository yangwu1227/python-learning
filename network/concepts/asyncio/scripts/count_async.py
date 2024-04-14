#!/usr/bin/env python3

import asyncio

async def async_count() -> None:
    """
    Asynchronously prints 'One', waits for 1 second, then prints 'Two'.
    """
    print('One')
    await asyncio.sleep(1)
    print('Two')
    
async def main() -> None:
    """
    Runs three async_count tasks concurrently.
    """
    await asyncio.gather(
        async_count(), async_count(), async_count()
    )
    
if __name__ == "__main__":
    import time
    import os
    start_time = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start_time
    file_name = os.path.basename(__file__)
    print(f"The module {file_name} executed in {elapsed:.2f} seconds")
