import json

import websockets
import requests
from mcdreforged.plugin.server_interface import PluginServerInterface

import kook_api.constsant.api_uri as api_uri
from kook_api.event import Event, MessageType
from kook_api.model.send_message import SendMsgReq


class KookApi:
    _ws_server: websockets
    _mcdr_server: PluginServerInterface
    _api_host: str
    _api_port: int
    _headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, mcdr_server, api_host, api_port):
        self._mcdr_server = mcdr_server
        self._api_host = api_host
        self._api_port = api_port

    def _get_api_address(self) -> str:
        return f"{self._api_host}:{self._api_port}"

    def _get_api_url(self, uri: str) -> str:
        return f"http://{self._api_host}:{self._api_port}{uri}"

    def _logger(self):
        return self._mcdr_server.logger

    def send_message_to_channel(self, req: SendMsgReq):
        body = json.dumps(req.get_dict())
        resp = requests.post(url=self._get_api_url(api_uri.MESSAGE_SEND), data=body, headers=self._headers)
        self._logger().debug(f"A message send to kook bot:{req.content}, target channel is:{req.target_id}")
        if resp.status_code != 200:
            self._logger().warning(f"Send message failed! Exception response is :'{resp.content}'")

    def reply(self, event: Event, content: str):
        req = SendMsgReq(target_id=event.channel_id, content=content)
        self.send_message_to_channel(req)
