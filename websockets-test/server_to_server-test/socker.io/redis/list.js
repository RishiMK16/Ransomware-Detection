const {Redis}=require('ioredis')

const client=new Redis()
l=[]
async function init() {
    await client.sadd('messages1','hi')
    await client.rpush('messages','how')
    await client.rpush('messages','bye')
    
    const res=await client.lrange('messages',0,-1)
    res.forEach((num)=>{
        l.push(num);
    })
    console.log(l)
    let respo=await client.expire('messages1')
    console.log(respo)
}

init()