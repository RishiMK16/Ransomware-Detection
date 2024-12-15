const express=require('express')
const app=express()
const {Server}=require("socket.io")
const {io}=require("socket.io-client")
const {toImgarray}=require('D:\\CODES\\Projects\\Ransomware_Desktop\\MicroServices\\controller\\packet_preprocessing.js')

const socket=new io("http://localhost:3333")

socket.on("connect",()=>{
    console.log("connected to sniffer server");
})

socket.on('packet_data',(packet)=>{
    hex_code=packet["payload"]
    socket.emit('preprocessed_payload',toImgarray(hex_code));
})