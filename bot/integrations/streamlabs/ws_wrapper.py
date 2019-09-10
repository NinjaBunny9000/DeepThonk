""" Provides SocketIO integration w/Streamlabs for stream alerts

Adds a task to the main bot loop to provide asynchronous functionality.
"""

from config.importer import bot, streamlabs_key
# from integrations.hue.api_wrapper import controller as hue
import logging
import asyncio
import socketio

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

log = logging.getLogger('deepthonk')
log.debug(f"{__name__} imported")

@sio.on('connect')
async def on_connect():
    log.info('[Integrations > Streamlabs] Socket.io Server... CONNECTERD!!')

@sio.on('event')
async def on_event(event):
    if event['type'] == 'bits':
        # bot.loop.create_task(hue.flash('green', attack=1, release=1, sustain=.1, times=8))
        pass

    if event['type'] == 'bits' and int(event['message'][0]['amount']) >= 60:
        # seconds = event['message'][0]['amount']
        # sender = event['message'][0]['name']
        pass
        # bot.loop.create_task(hardmode_task(sender, seconds))
    
    if event['type'] == 'follow':
        log.debug('follow was detected')
        # bot.loop.create_task(hue.flash('purple', times=4))
        pass

    if event['type'] == 'subscription':
        # bot.loop.create_task(hue.flash('lightblue', times=4))
        pass

    if event['type'] == 'donation':
        # bot.loop.create_task(hue.flash('yellow', times=4))
        pass

    if event['type'] == 'host':
        # bot.loop.create_task(hue.flash('red', times=10))
        pass

    if event['type'] == 'raid':
        # bot.loop.create_task(hue.flash('red', times=10))
        pass


@sio.on('disconnect')
async def on_disconnect():
    log.error(f"y u disconnect?")
    

async def listen_streamlabs():
    await sio.connect(f"https://sockets.streamlabs.com?token={streamlabs_key}")
    await sio.wait()


bot.loop.create_task(listen_streamlabs())


if __name__ == '__main__':
    loop.run_until_complete(listen_streamlabs())