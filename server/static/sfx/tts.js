// handle tts from #tts command triggers and events (soon)
socket.on( 'tts trigger', function(msg) {
    socket.emit( 'my event', {
      data: msg
    } )

    const chirp = "/static/sfx/other/tng_chirp.mp3"

    addToQueue(chirp, `https://api.streamelements.com/kappa/v2/speech?voice=Salli&text=${msg}`);

    // TODO time-delay for the tts?
  })
