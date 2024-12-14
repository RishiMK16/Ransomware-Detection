const {io} = require('socket.io-client');

const socket=new io('http://localhost:3000');

socket.on('connect',()=>{
    console.log("connected to server with id ",socket.id);
    socket.emit('client-message','connected');
})
l=[]
socket.on('servermessage',(message)=>{
    if(l.length>20){
        socket.emit('more-message',`exceeded : ${l.length}`);
    }
    l.push(message);
    console.log(l);

})