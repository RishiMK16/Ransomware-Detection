const express=require('express')
const app=express()
const {Server}=require("socket.io")
const {io}=require("socket.io-client")
const {toImgarray}=require('D:\\CODES\\Projects\\Ransomware_Desktop\\MicroServices\\controller\\packet_preprocessing.js')
const http=require('http');


//CLIENT
const socketClient=new io("http://localhost:3333")

socketClient.on("connect",()=>{
    console.log("connected to sniffer server");
})


//SERVER
app.get('/health',(req,res)=>{
    res.send({'health':"healthy"})
})
const server=http.createServer(app)
const ws=new Server(server)

ws.on('connection',(socket)=>{
    console.log("connected to AI instance of id : ",socket.id)

    socketClient.on('packet_data',(packet)=>{
        hex_code=packet["payload"]
        socket.emit('image_array',toImgarray(hex_code))
    })

})



server.listen(3334,()=>{
    console.log("listening on port 3334")
})