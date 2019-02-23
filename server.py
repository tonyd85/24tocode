from collections import defaultdict

import falcon
import json
from falcon_cors import CORS


cors = CORS(allow_all_origins=True)
api = falcon.API(middleware=[cors.middleware])

sliding_window = defaultdict(list)

def add_headers(response):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Content-type', 'application/json')

headers={'Content-Type': 'application/json'}

window_length=1000
def get_vectors(sliding_window):
    if len(sliding_window) == 0:
        return {
            'x': [],
            'y': []
        }
    kvpairs = [
        (k, measure_window(v[-window_length:]) )
        for k,v in sliding_window.items() ]
    sorted_pairs = sorted(kvpairs, key=lambda x: x[1])
    x, y = zip(*kvpairs) 
    return {
        'x': x,
        'y': y
    }

def measure_window(window):
    return 100 * sum(window) / len(window)


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

        data = get_vectors(sliding_window)
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
        for component in valid_components:
            if data['component'] == component:
                sliding_window[component].append(1)
            else:
                sliding_window[component].append(0)
        resp.body = json.dumps({'data': {
            'counts': '' 
        }})
        add_headers(resp)
        resp.status = falcon.HTTP_200

resource = Resource()
api.add_route('/data', resource)
