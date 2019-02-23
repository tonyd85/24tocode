from collections import Counter

import falcon
import json
from falcon_cors import CORS

cors = CORS(allow_all_origins=True)

api = falcon.API(middleware=[cors.middleware])

def add_headers(response):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Content-type', 'application/json')

headers={'Content-Type': 'application/json'}


component_defect_counts = Counter()

def get_vectors(counter):
    if len(counter.keys()) == 0:
        return {'x': [], 'y': []}
    arr = zip(counter.keys(), counter.values())
    sorted_arr = sorted(arr, key=lambda x: -x[1])
    x, y = zip(*sorted_arr)
    return {
        'x': x,
        'y': y
    }

valid_components = [
    'PN-0489',
    'PN-9932',
    'PN-9284',
    'PN-8867',
    'PN-0034',
    'PN-7121',
    'PN-8532',
    'PN-6630',
    'PN-9910',
    'PN-3491',
    'PN-2533',
    'PN-0303'
]

class Resource:

    def on_get(self, req, resp):
        data = req.params

        data = get_vectors(component_defect_counts)
        data['type'] = 'bar'
        payload = {
            'component_defect_counts': [data]
        }
        print(payload)

        resp.body = json.dumps(payload)
        print(resp.body)
        add_headers(resp)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Handles POST requests"""
        body = req.stream.read().decode('utf-8')
        data = json.loads(body)
        print(data)
        if data['component'] in valid_components:
            component_defect_counts.update([data['component']])
        resp.body = json.dumps({'data': {
            'counts': dict(component_defect_counts)
        }})
        add_headers(resp)
        resp.status = falcon.HTTP_200

resource = Resource()
api.add_route('/data', resource)
