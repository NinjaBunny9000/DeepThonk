""" Interfaces with the IRL robot via the webserver (SocketIO)

Emits socketio events, tied to chat commands, to the webserver (Flask), which
emits socketio events to the microcontroller (SAMD/CircuitPython + ESP32)
"""

import socketio
from config.importer import bot, data
from utils.logger import loggymclogger as log
import logging


log.debug(f"{__name__} loaded")
sfx_files_with_extension = []

sio = socketio.AsyncClient(logger=log)

# comment to enable verbose EngineIO comments in the console
logger = logging.getLogger('engineio')
logger.setLevel(level=logging.WARNING)


@sio.on('connect')
async def on_connect():
    import commands.tts  # only import this if the websocket connection is made
    log.debug(f"{__name__}.... CONNECTERD!")
    await sio.emit('connect',{'data':'CONNECTERD!'})
    await sio.emit('get_sfx')
    await sio.emit('get_randos') # TODO get a list of folders (random sfx) from the server via ws


@sio.on('response')
async def on_repsponse(data):
    log.debug(f"[MSG RCVD] {data}")


@sio.on('heres_yo_randos')
async def heres_yo_randos(data):
    log.debug(f"RANDO EFFECTS RECIEVED: {data}")

@sio.on('send_sfx')
async def on_send_sfx(data):
    from commands.sfx import SoundEffect
    # print(f"SFX RCVD:")
    # print(data)
    global sfx_files_with_extension
    sfx_files_with_extension = data  # i think this will fail
    for sfx_cmd in sfx_files_with_extension:
        # print(f"passing in {sfx_cmd}")
        SoundEffect(sfx_cmd)
    SoundEffect.generate_sfx_list()


async def listen_socketio_server():
    try:
        await sio.connect('http://localhost:6969')  # uncomment for local hosting
        # await sio.connect('http://0.0.0.0:6969')  # uncomment remote hosting
        await sio.wait()
    except:
        log.warning("Server OFFLINE. Bot functionality reduced.")


async def emit_tts(text):
    if data.get_setting('tts'):
        await sio.emit(event='tts', data=text)


async def emit_sfx(command):
    await sio.emit(event='sfx', data=command)  # DEBUG should just be 'sfxtest' for now


async def emit_stream_event(event):
    # await sio.emit(event='stream event', data=event)
    log.debug(f"emitting {event} event")
    await sio.emit(event=event)


def create_task():
    'Enable SIO to run concurrently with TwitchIO'
    bot.loop.create_task(listen_socketio_server())

create_task()
