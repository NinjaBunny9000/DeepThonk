var socket = io.connect();
socket.on( 'connect', function() {
  socket.emit( 'my event', {
    data: 'User DERP DERP Connected'
  })
})


socket.on( 'sfx trigger', msg => {
    addToQueue(`/static/sfx/hooks/${msg}.mp3`);
  })