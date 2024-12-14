const {WebSocket,WebSocketServer}=require('ws');
const express=require('express');
const app=express();
const http=require('http');

app.get('/*',(req,res)=>{
    res.json({'message':'I am healthy'});
})
const server=http.createServer(app);
const ws=new WebSocketServer({server});
ws.on('connection',(socket)=>{
    socket.on('error',()=>console.error);
    console.log('connected to socket');

    socket.on('message',(message)=>{
        //ws.emit('server-message',message);
        ws.clients.forEach((client)=>{
            if(client.readyState==WebSocket.OPEN){
                client.send(message);
            }
        })
    })

    socket.send("hello from server");
})
server.listen(1200,()=>{
    console.log("listening on port 1200");
})
