#!/usr/bin/env python3
import asyncio
import socket
from keyword import kwlist
from typing import Tuple

# Set maximum length of keyword for domains
MAX_KEYWORD_LEN = 4

async def probe(domain: str) -> Tuple[str, bool]:
    """
    Check domains to see if they are available.

    Parameters
    ----------
    domain : str
        A domain name constructed using a python keyword ending with .dev

    Returns
    -------
    Tuple[str, bool]
        A tuple (domain name, boolean), where True means the domain is resolved and False means that it may be available.
    """
    # Get reference to the event loop
    loop = asyncio.get_running_loop()
    try:
        # This coroutine returns (family, type, proto, canonname, sockaddr), used to connect to the given address via socket
        await loop.getaddrinfo(host=domain, port=None)
    except socket.gaierror:
        # If the domain is not a valid hostname, it may be available
        return (domain, False)
    return (domain, True)

async def main() -> None:
    
    # Generator of keywords and domain names
    names = (key_word for key_word in kwlist if len(key_word) <= MAX_KEYWORD_LEN)
    domains = (f"{name}.dev".lower() for name in names)
    # List of coroutines objects
    coros = [probe(domain=domain) for domain in domains]

    # Yield coroutines, which return the results of the coroutines, in the order they are completed
    for coro in asyncio.as_completed(coros):
        # If `coro` raised an unhandled exception, it would be re-raised here
        domain, found = await coro
        indicator = '+' if found else ' '
        print(f"{indicator} {domain}")

if __name__ == "__main__":
    
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"The program executed in {elapsed: .2f} seconds")
