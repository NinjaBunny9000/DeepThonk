socket.on( 'sfx trigger', msg => {
    addToQueue(`/static/sfx/hooks/${msg}.mp3`);
  })