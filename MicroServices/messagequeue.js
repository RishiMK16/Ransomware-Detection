const {Redis}=require('ioredis');

const client=new Redis();

const mq_queue=async(packet)=>{
    await client.lpush("test_queue",packet);
}

const mq_pop=async()=>{
    let array=await client.rpop("test_queue")
    console.log(array);
}


mq_queue("anannnyaaaa");
mq_pop();