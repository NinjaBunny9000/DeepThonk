socket.on( 'sfx trigger', msg => {
    addToQueue(`/static/sfx/hooks/${msg}`);
  })

socket.on( 'raid triggered', msg => {
    addToQueue(`/static/sfx/other/raid.mp3`);
    // addToQueue(`/static/sfx/hooks/doot.mp3`);
    // console.log('raid detected. d00ting.')
  })