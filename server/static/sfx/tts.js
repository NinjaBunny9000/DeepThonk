// // handle tts from #tts command triggers and events (soon)
// socket.on( 'tts trigger', function(msg) {
//     socket.emit( 'my event', {
//       data: msg
//     } )

//     const chirp = "/static/sfx/other/tng_chirp.mp3"

//     addToQueue(chirp, `https://api.streamelements.com/kappa/v2/speech?voice=Salli&text=${msg}`);

//     // TODO time-delay for the tts?
//   })


// handle tts from #tts command triggers and events (soon)
socket.on( 'tts trigger', function(msg) {
  console.log('TTS TEST RCVD AND STUFF: ' + msg)
  socket.emit( 'my event', `TTS TRIGGERED: ${msg}` )
  playTTS(msg)
  // TODO time-delay for the tts?
})