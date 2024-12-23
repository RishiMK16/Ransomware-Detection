const {data}=require('./TokensLoader.js');
const {Redis}=require('ioredis');

const client=new Redis();

function preprocess_payload(l){
    if(l.length<784){
        let zeroes=784-l.length;
        for(let i=0;i<zeroes;i++){
            l.push(0);
        }
        return l
    }else{
        newl=[]
        for(let i=0;i<784;i++){
            newl.push(l[i])
        }
        return newl
    }
}

function pairer(string){
    l=[]
    for(let i=0;i<string.length-1;i++){
        let temp=string[i]+string[i+1]
        l.push(temp);
    }
    return l
}


function tokenize(string){
    let pairs=pairer(string)
    l=[]
    for(let i=0;i<pairs.length;i++){
        let val=data[pairs[i]]
        l.push(val)
    }
    return l;
}

function reshapeTo3D(array, rows, cols, depth) {
    if (array.length !== rows * cols * depth) {
        throw new Error("Array size does not match the specified dimensions.");
    }

    const reshapedArray = [];
    for (let i = 0; i < rows; i++) {
        const row = [];
        for (let j = 0; j < cols; j++) {
            row.push([array[i * cols + j]]); 
        }
        reshapedArray.push(row);
    }
    return reshapedArray;
}

function toImgarray(string){
    l=tokenize(string)
    arr=preprocess_payload(l)
    return arr
}


const mq_queue=async(packet)=>{
    await client.lpush("test_queue",packet);
}

const mq_pop=async()=>{
    let array=await client.rpop("test_queue")
    console.log(array);
}


module.exports={toImgarray,push:mq_queue,pop:mq_pop}