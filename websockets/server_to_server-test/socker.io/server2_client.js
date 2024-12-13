const {io} = require('socket.io-client');

const socket=new io('http://localhost:3000');

socket.on('connect',()=>{
    console.log("connected to server with id ",socket.id);
    socket.emit('client-message','hi from client');
})

socket.on('serverMessage',(message)=>{
    console.log("server said ",message);
})