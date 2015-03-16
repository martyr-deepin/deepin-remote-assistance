
import json

def handle_cmd_event(ws, msg):
    event = json.loads(msg)
    peer_id = event['id']
    print('local Peer Id:', peer_id)
    # TODO: emit peerReceived signal
    return []
