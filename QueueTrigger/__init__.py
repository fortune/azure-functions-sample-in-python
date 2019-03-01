import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    """
    Azure Storage Queue をトリガとする関数。キューにメッセージが追加されたときに
    起動され、メッセージを処理できる。
    """
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
