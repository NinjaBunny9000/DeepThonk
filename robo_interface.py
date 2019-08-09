""" Interfaces with the IRL robot via the webserver (SocketIO)

Emits socketio events, tied to chat commands, to the webserver (Flask), which
emits socketio events to the microcontroller (SAMD/CircuitPython + ESP32)
"""

import socketio
from config.importer import bot
from utils.logger import loggymclogger as log
import logging

log.debug(f"{__name__} loaded")

sio = socketio.AsyncClient(logger=log)

# comment to enable verbose EngineIO comments in the console
logger = logging.getLogger('engineio')
logger.setLevel(level=logging.WARNING)


@sio.on('connect')
async def on_connect():
    log.debug(f"{__name__}.... CONNECTERD!")
    await sio.emit('connect',{'data':'CONNECTERD!'})


@sio.on('response')
async def on_repsponse(data):
    log.debug(f"[MSG RCVD] {data}")


async def listen_socketio_server():
    await sio.connect('http://localhost:6969')
    await sio.wait()


async def emit_expression(expression):
    await sio.emit(event='expression', data=expression)


async def emit_tts(text):
    await sio.emit(event='tts', data=text)


async def emit_stream_event(event):
    await sio.emit(event='stream event', data=event)


def create_task():
    bot.loop.create_task(listen_socketio_server())

create_task()
