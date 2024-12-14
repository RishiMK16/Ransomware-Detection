//import exp from 'constants'
const http=require("http");
const express=require('express')
const app=express()
const {Server}=require("socket.io");

app.get('/health',(req,res)=>{
    res.send("healthy")
})

app.get('/chat',(req,res)=>{
    res.sendFile("D:\\CODES\\Projects\\Ransomware_Desktop\\public\\index.html")
})
const server=http.createServer(app)
const ws=new Server(server)
ws.on("connection",(socket)=>{
    console.log("connected to socket ", socket.id);
    socket.on('user-message',message=>{
        console.log(message);
        ws.emit("message",message);
    ;})
})
server.listen(2900,()=>console.log("listening"));