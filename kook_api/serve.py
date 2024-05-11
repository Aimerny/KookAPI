import asyncio
from asyncio import AbstractEventLoop
import time

import websockets
from mcdreforged.api.decorator import new_thread
from mcdreforged.plugin.server_interface import PluginServerInterface

from kook_api import Config, content_parser

connect: bool = True
event_loop: AbstractEventLoop
ws_task: asyncio.Task
ws_server: websockets


async def connect_to_kook(server: PluginServerInterface, config: Config):
    async with websockets.connect(f"ws://{config.kook_host}:{config.kook_port}/ws") as ws:
        global ws_server
        ws_server = ws

        while connect:
            receive = await ws.recv()
            content_parser.event_parse(receive, server, ws_server)


@new_thread('Kook API')
def start(server: PluginServerInterface, config: Config):
    global event_loop, ws_task
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    ws_task = event_loop.create_task(connect_to_kook(server, config))
    try:
        server.logger.info('Kook API started')
        event_loop.run_until_complete(ws_task)
    except asyncio.CancelledError:
        server.logger.info("old websocket connection closed!")
        pass


def stop(server: PluginServerInterface):
    global connect
    connect = False
    server.logger.info('Kook API closed')
    # interrupt old websocket thread
    ws_task.cancel()
    time.sleep(0.5)


def send(msg: str):
    async def ws_send(m: str):
        await ws_server.send(m)

    asyncio.run(ws_send(msg))
