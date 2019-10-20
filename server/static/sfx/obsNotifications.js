const obs = new OBSWebSocket();

obs.connect({
    // Either port forward or sign up for ngrok and let it forward for you.
    address: 'localhost:4444',
    // address: '<redacted>:4444', // The remote IP of <redacted> ??
    password: 'password'
})
.then(() => {
    console.log('logged in to obs');
    // playTTS('Logged in to OBS');
})
.catch((err) => {
    console.log(err);
    playTTS('Failed to connect to OBS');
});


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
    // playTTS(text, voice);
    // emit sio event instead
    socket.emit('tts trigger', text)
    console.log(text);
}

obs.on('TransitionBegin', transitionBegin); 