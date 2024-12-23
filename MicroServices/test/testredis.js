const express=require('express')
const app=express()
const {Server}=require("socket.io")
const {io}=require("socket.io-client")
const {toImgarray,push,pop}=require('D:\\CODES\\Projects\\Ransomware_Desktop\\MicroServices\\controller\\packet_preprocessing.js')
const http=require('http');
const {Redis}=require('ioredis');

const client=new Redis()


//CLIENT
// const socketClient=new io("http://localhost:3333")

// socketClient.on("connect",()=>{
//     console.log("connected to sniffer server");
// })

// socketClient.on('packet_data',async(packet)=>{
//     hex_code=packet["payload"]
//     array=toImgarray(hex_code)
//     const serializedArray = JSON.stringify(array);
//     await client.lpush("test_queue",serializedArray);
//     console.log(array);
//         //socket.emit('image_array',toImgarray(hex_code))
// })

const get =async()=>{
    let x=await client.rpop("test_queue")
    const deserializedArray = JSON.parse(x);
    console.log(deserializedArray);
}

get()