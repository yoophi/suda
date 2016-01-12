from flask import jsonify

from sample.api_1_0 import api


@api.route('/samples')
def samples():
    return jsonify({
        'items': [
            {'id': 1, 'text': 'foo'},
            {'id': 2, 'text': 'bar'},
            {'id': 3, 'text': 'hello, world'},
        ]
    })
