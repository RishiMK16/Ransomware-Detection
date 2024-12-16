const express=require('express');
const app=express();
const {Server}=require('socket.io');
const http=require('http');
const cors = require('cors');

app.use(cors());
l=[]
for(let i=0;i<100;i++){
   l[i]=i 
}
l=[] 
for(let i=0;i<1000;i++){
    l[i]=i;
}
app.get('/getList',(req,res)=>{
    res.send({'message':l})
})

app.get('/socket',(req,res)=>{
    res.sendFile("D:\\CODES\\Projects\\Ransomware_Desktop\\public\\socket.html")
})

const server=http.createServer(app);
const ws=new Server(server);
ws.on("connection",(socket)=>{
    console.log("connected to ",socket.id);
    socket.on('client-message',(message)=>{
        for(let i=0;i<100;i++){
            socket.emit('servermessage',l[i])
        }
    })
    socket.on('more-message',(mess)=>{
        console.log(mess);
    })
})


server.listen(3000,()=>console.log('listening on port 3000'))