import requests
from time import sleep


def retry_req(func, **kwargs):
    # wrapper to keep retrying api calls, while we get connection errors
    # trying 10 times to connect
    count = 10
    sleep(0.25)
    while count > 0:
        try:
            res = func(**kwargs)
            if count < 10:
                   print('')
            return res
        except Exception as e:
            sleep(0.5)
            count -= 1
            if count == 0:
                # retries failed, throws exception
                print(f"Connection failed, {count} tries failed: no retry")
                raise RuntimeError("10 retries failed") from e
            else:
                print('.', end='')


def request(**kw):
    # wrap request function
    return retry_req(requests.request, **kw)
