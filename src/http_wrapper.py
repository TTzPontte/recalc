import logging
from .encoder import dumps


def http(fn):
    def wrapped(event, context):
        try:
            response = fn(event, context)
            return {
                'statusCode': 200,
                'body': dumps(response)
            }
        except Exception as e:
            logging.exception(str(e))
            return {
                'statusCode': 400,
                'body': dumps({
                    'error': str(e)
                })
            }
    return wrapped

