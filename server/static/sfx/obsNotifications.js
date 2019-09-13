let Queue = {
    isPlaying : false,
    list : []
}

const obs = new OBSWebSocket();
const events = new EventEmitter3();

// obs.connect({ address: 'localhost:4444', password: 'password' })
// .then(() => {
//     console.log('logged in to obs');
// });

// obs.on('error', err => {
//     console.error('socket error:', err);
// });

obs.connect({
    address: 'localhost:4444',
    // address: '<redacted>:4444', // The remote IP of <redacted> ??
    // Either port forward or sign up for ngrok and let it forward for you.
    password: 'password'
})
.then(() => {
    console.log('logged in to obs');
    playTTS('Logged in to OBS');
})
.catch((err) => {
    console.log(err);
    playTTS('Failed to connect to OBS');
});

/**
 * An interface that represents an audio-processing graph built from audio modules
 * linked together
 * @see http://mdn.io/AudioContext
 */
const audioCtx = new AudioContext();

/**
 * Cache sound effects that will be re-used.
 * 
 * @type {Map<String, AudioBuffer>}
 * @see http://mdn.io/Map
 */
const soundCache = new Map();

/**
 * Load a sound file from a URL and create an AudioBuffer instance that can be
 * played to an AudioContext object.
 * 
 * @param {string} location The URL location of the sound to load.
 * @returns {Promise<AudioBuffer>}
 */
function loadSound(location, skipCache=false) {
    // Check for the sound in the cache
    if(soundCache.has(location)) {
        // Get and return the AudioBuffer from the cache.
        const audioBuf = soundCache.get(location);
        return Promise.resolve(audioBuf);
    }
    // Download the audio from the internet or a local server.
    return fetch(location)
    .then(res => {
        // Get the data from the response as an ArrayBuffer.
        return res.arrayBuffer();
    })
    .then(arrayBuf => {
        // Ask the AudioContext to decode the ArrayBuffer into an AudioBuffer
        return audioCtx.decodeAudioData(arrayBuf);
    })
    .then(audioBuf => {
        // Store the AudioBuffer into the cache if it's enabled.
        if (!skipCache) { soundCache.set(location, audioBuf); }
        return audioBuf;
    })
    .catch(err => {
        // Log any errors and return null.
        console.error(err);
        return null;
    });
}

/**
 * Play a sound. Either pass the URL of the location and it will be loaded or an
 * AudioBuffer instance. This will immediately play the audio directly into the
 * speakers.
 * 
 * @param {string|AudioBuffer} audioBuf The audio URL or AudioBuffer to play.
 * @returns {Promise}
 */
function playSound(audioBuf, skipCache) {
    if(audioBuf === null) {
        return;
    }
    if(typeof audioBuf === 'string') {
        return loadSound(audioBuf, skipCache)
        .then(playSound);
    }
    return new Promise(resolve => {
        const source = audioCtx.createBufferSource();
        source.buffer = audioBuf;
        source.connect(audioCtx.destination);
        source.start(audioCtx.currentTime);
        source.onended = resolve;
    });
}

/**
 * Cues teh queue.
 */

async function cueQueue() {
   
    if (!Queue.list.length) {  // handle list being empty
        return;
    } else if (Queue.isPlaying) { // handle if it's playing, then play next
        // create a promise that waits for the 'queue-next' event then plays the queue
        return once(events, 'queue-next').then(cueQueue);
    }

    Queue.isPlaying = true;  // mark the queue as playing
    const listItem = Queue.list.shift(); // shift the list into another var thing

    // iterate through list of items in the queue and play them
    for (const item of listItem.items) {
        await playSound(item);
    }

    // clean-up
    Queue.isPlaying = false;
    events.emit('queue-next');
}

/**
 * Loads audios into a queue.
 * 
 * @param  {...any} items 
 * 
 */

async function addToQueue(...items) {
    // handle if the audio passed in was a string (file location or url)
    for(const [ i, n ] of items.entries()) {
        if (typeof n === 'string') {
            items[i] = await loadSound(n);
        }
    }
    Queue.list.push({ items });
    cueQueue();
}

function playTTS(text, voice = 'Salli') {
    /**
     * object with methods endcodes data structures as URL search param
     * @see https://mdn.io/URLSearchParams
     */
    const qs = new URLSearchParams({ voice, text });
    const url = 'https://api.streamelements.com/kappa/v2/speech?' + qs;
    addToQueue(url);
}

// This event will fire after the stinger, use "TransitionBegin" for the start of
// the transition.
// obs.on('SwitchScenes', () => {

/**
 * A scene transition has begun. This will fire at the start of the transition
 * rather than after with SwitchScenes.
 * 
 * @param {object} data The data from the event.
 * @param {number} data.duration Duration of the transition in milliseconds.
 * @param {string} data.name The name of the transition.
 * @param {string} data.fromScene Name of the scene it's transitioning from.
 * @param {string} data.toScene Name of the scene it's transitioning to.
 * @param {string} data.streamTimecode Formatted timestamp of the stream that
 * the transition started.
 */
function transitionBegin(data) {
    // console.log(data);
    const { fromScene, toScene } = data; // FAX: this is Destructuring™
    const voice = 'Salli';
    const ttsDict = {
        maint: `Signal quality has changed. Going into maintenance mode.`,
        refresh: 'Possible data corruption. Refreshing source. Please stand ' +
            'by...',
        irl: `Resuming stream..`
    };
    const text = ttsDict[toScene];
  
    if(!text) {
        console.log(
            'no scene change tts transition configured.',
            `"${fromScene}" -> "${toScene}"`
        );
        return;
    }
    playTTS(text, voice);
}

obs.on('TransitionBegin', transitionBegin);
