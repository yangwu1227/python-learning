from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPStatus
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from typing import Union, MutableSequence

# ------------------------ Get the status of a website ----------------------- #


def get_website_status(url: str) -> Union[int, str, BaseException]:
    # Handle connection errors
    try:
        # Open a connection to the server with a timeout
        with urlopen(url, timeout=3) as connection:
            # Get the response code, e.g. 200
            code = connection.getcode()
            return code
    except HTTPError as e:  # Raised when HTTP error occurs
        return e.code
    except URLError as e:  # URLError could be raised if we are unable to connect
        return e.reason
    except Exception as e:  # Catch all other exceptions
        return e


# --------------- Interpret an HTTP response code into a status -------------- #


def get_status(code: Union[BaseException, int, str]) -> str:
    if code == HTTPStatus.OK:
        return "OK"
    return "ERROR"


# -------------------- Check status of a list of websites -------------------- #


def check_status_urls(urls: MutableSequence[str]) -> None:
    # Create the thread pool with as many workers as there are URLs
    with ThreadPoolExecutor(len(urls)) as executor:
        # Issue each task, map of futures to urls
        future_to_url = {
            executor.submit(get_website_status, url): url for url in urls
        }  # Each key is a future object for a given, which is its value
        # Get results as they are available, since we do not care about order or return values
        for future in as_completed(future_to_url):
            # Get the url for the future
            url = future_to_url[future]
            # Get the status for the website
            code = future.result()
            # Interpret the status
            status = get_status(code)
            # Report status
            print(f"{url:20s}\t{status:5s}\t{code}")


# Protect the entry point
if __name__ == "__main__":
    # list of urls to check
    urls = [
        "https://twitter.com",
        "https://google.com",
        "https://facebook.com",
        "https://reddit.com",
        "https://youtube.com",
        "https://amazon.com",
        "https://wikipedia.org",
        "https://ebay.com",
        "https://instagram.com",
        "https://cnn.com",
    ]
    # check all urls
    check_status_urls(urls)
