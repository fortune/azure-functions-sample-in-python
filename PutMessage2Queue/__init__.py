import logging
  
import azure.functions as func

"""
出力バインディングに Azure Storage Queue を追加して、
HTTP リクエスト name で渡された値をキューにセットするサンプル。

出力バインディング設定ファイル function.json を直接編集している。
"""


def main(req: func.HttpRequest,
         msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        msg.set('Name passed to the function: ' + name)
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )