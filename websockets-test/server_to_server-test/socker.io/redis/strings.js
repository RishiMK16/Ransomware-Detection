const {Redis}=require('ioredis')

const client=new Redis();
async function init(){
    await client.expire('name:1',10);//to expire key after 10 seconds
    const res=await client.get('name:1');
    console.log(res)
}

init()