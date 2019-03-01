import logging
import os, time

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pid = os.getpid()
    start_time = time.time()
    while True:
        if time.time() - start_time > 3:
            break

    return func.HttpResponse('pid = ' + str(pid))

