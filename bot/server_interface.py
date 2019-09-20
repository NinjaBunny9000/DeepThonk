""" Interfaces with the IRL robot via the webserver (SocketIO)

Emits socketio events, tied to chat commands, to the webserver (Flask), which
emits socketio events to the microcontroller (SAMD/CircuitPython + ESP32)
"""

import socketio
from config.importer import bot
from utils.logger import loggymclogger as log
import logging


log.debug(f"{__name__} loaded")

list_of_sfx_files = []

sio = socketio.AsyncClient(logger=log)

# comment to enable verbose EngineIO comments in the console
logger = logging.getLogger('engineio')
logger.setLevel(level=logging.WARNING)


@sio.on('connect')
async def on_connect():
    import tts  # only import this if the websocket connection is made
    log.debug(f"{__name__}.... CONNECTERD!")
    await sio.emit('connect',{'data':'CONNECTERD!'})
    await sio.emit('get_sfx')


@sio.on('response')
async def on_repsponse(data):
    log.debug(f"[MSG RCVD] {data}")


@sio.on('send_sfx')
async def on_send_sfx(data):
    from sfx import SoundEffect
    print(f"SFX RCVD:")
    # print(data)
    global list_of_sfx_files
    list_of_sfx_files = data  # i think this will fail
    for sfx_cmd in list_of_sfx_files:
        SoundEffect(sfx_cmd)
    SoundEffect.generate_sfx_list()


async def listen_socketio_server():
    try:
        await sio.connect('http://0.0.0.0:6969')
        await sio.wait()
    except:
        log.warning("Server OFFLINE. Bot functionality reduced.")


async def emit_tts(text):
    await sio.emit(event='tts', data=text)


async def emit_sfx(command):
    await sio.emit(event='sfx', data=command)  # DEBUG should just be 'sfxtest' for now


async def emit_stream_event(event):
    await sio.emit(event='stream event', data=event)


def create_task():
    'Enable SIO to run concurrently with TwitchIO'
    bot.loop.create_task(listen_socketio_server())

create_task()
