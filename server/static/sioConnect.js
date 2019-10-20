// connect to flask socketio socketything
var socket = io.connect();
    socket.on( 'connect', function() {
        socket.emit( 'my event', {
            data: 'BROWSER SOURCE connection detected.'
        })
    });