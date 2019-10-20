from flask import Flask, render_template
from flask_socketio import SocketIO
from conf import secret_key
from sfx import list_of_sfx_files, sfx_with_extentions
from utils.logger import loggymclogger as log


# init the flask app
app = Flask('__name__')
app.config['SECRET_KEY'] = secret_key


# init socketio server
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/obs-source/')
def obs_source():
    return render_template('obs-source.html')


def messageReceived(methods=['GET', 'POST']):
    # print('message was received!!!') 
    pass

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    log.debug(f"RCVD: 'my event' // DATA: {str(json)}")
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('tts')
def tts_event(data, methods=['GET', 'POST']):
    msg = str(data)
    socketio.emit('tts trigger', msg)
    log.debug(f"TTS Triggered => {msg}")


@socketio.on('sfx')
def sfx_event(command, methods=['GET', 'POST']):
    'Recievs SFX requests from bot app & triggers SFX on the Browser Source'
    sfx_command = str(command)
    socketio.emit('sfx trigger', sfx_command)
    log.debug(f"SFX Triggered => {sfx_command}")


@socketio.on('get_sfx')
def get_sfx_event(methods=['GET', 'POST']):
    'Sends list of SFX files so the bot can generate chat commands/objects.'
    log.debug(f"Bot application requested SFX files to generate commands.")
    # socketio.emit('send_sfx', list_of_sfx_files) # <- list serialized as json
    socketio.emit('send_sfx', sfx_with_extentions) # <- list serialized as json

@socketio.on('raid')
def raid_event(methods=['GET', 'POST']):
    log.debug(f"RAID OCCURRRRRED")
    socketio.emit('raid triggered')


if __name__ == "__main__":
    socketio.run(app, debug=True, port='6969') # run w/socketio # running locally
    # socketio.run(app, host='0.0.0.0', debug=True, port='6969') # running remotely