const express=require('express')
const app=express()
const {Server}=require("socket.io")
const {io}=require("socket.io-client")
const {toImgarray,push,pop}=require('D:\\CODES\\Projects\\Ransomware_Desktop\\MicroServices\\controller\\packet_preprocessing.js')
const http=require('http');
const {Redis}=require('ioredis');

const client=new Redis()


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

    socketClient.on('packet_data',async(packet)=>{
        hex_code=packet["payload"]
        array=toImgarray(hex_code)
        const serializedArray = JSON.stringify(array);
        await client.lpush("test_queue",serializedArray);
        
    })

    socket.on("AI_resp",async(resp)=>{
        if(resp==="True"){
            x=await client.rpop('test_queue');
            socket.emit('image_array',{ payload: x })
        }
    })

    

    socket.on('prediction',(pred)=>{
        if(pred===1){
            socketClient.emit('block',"True")
        }else{
            socketClient.emit('block',"False");
        }
    })

})



server.listen(3334,()=>{
    console.log("listening on port 3334")
})