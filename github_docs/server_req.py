from warnings import warn
import websocket
import json

def server_req(ws_server_requests: dict, project_id, uri=uri_to_talk_to, ignore_timeout=True, timeout=3):
    ws = websocket.WebSocket()
    ws_server_requests["project_id"] = project_id
    ws.connect(uri, timeout=timeout)
    ws.send(json.dumps(ws_server_requests))
    if ignore_timeout:
        try:
            return ws.recv()
        except websocket._exceptions.WebSocketTimeoutException:
            warn("timed out, canceling operation")
            return None
    else:
        return ws.recv()

def get_var(project_id, Vname="TO PYTHON"):
    print("trying to grab var")
    return server_req({"method": "api.get.var", "name":Vname}, project_id)

def hand_shake(pid):
    return server_req({"method": "handshake"}, pid)
