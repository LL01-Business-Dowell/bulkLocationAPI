// import startConsumer from "./kafka-consumer.js";
// await startConsumer().catch(console.error);
// const { Kafka } = require('kafkajs');
// const { DatacubeApiClient } = require('./Datacube.js');
import { Kafka } from 'kafkajs';
import DatacubeApiClient from './Datacube.js';
import Datacubeservices from './datacube_db.js';
const kafka = new Kafka({
    clientId: 'location-service',
    brokers: ['kafka:9092']
    // brokers: ['localhost:9092']
});
const producer = kafka.producer();
async function sendToKafka(topic, message) {
    await producer.connect();
    await producer.send({
        topic,
        messages: [{ value: JSON.stringify(message) }],
    });
    await producer.disconnect();
}
async function startConsumer() {


    const consumer = kafka.consumer({ groupId: 'group1' });
    // const consumer_get_details = kafka.consumer({ groupId: 'change-location-group' });
    await consumer.connect();
    // await consumer_get_details.connect();
    await consumer.subscribe({ topic: 'topic_1', fromBeginning: false });
    // await consumer_get_details.subscribe({ topic: 'get_details', fromBeginning: false });

    // Instantiate the MongoApiClient with your API's base URL
    // const datacubeClient = new DatacubeApiClient('https://datacube.uxlivinglab.online/'); // Update with actual base URL
    const datacubeClient = new Datacubeservices("76092219-c570-4c86-88f0-efa63966e06b");// Update with actual base URL

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            // const msg = JSON.parse(message.value.toString());
            // console.log(`Received message: ${JSON.stringify(msg)}`);

            try {
                const rawMessage = message.value.toString();
                const msg = JSON.parse(rawMessage);
                // console.log(`Raw message received: ${rawMessage}`);
                // console.log(`Raw message received keys: ${Object.keys(message)}`);
                // console.log(`Raw value received: ${message.value}`);
                // console.log(`Raw value.action received: ${message.value.action}`);
                // console.log(`Raw action received: ${message.action}`);
                // console.log(`Received msg.action : ${msg.action}`);
                let response;
                const { action, dbName, collName, ...params } = msg;

                switch (action) {
                    case 'insert':
                        // response = await datacubeClient.insertData(dbName, collName, params.data);
                        response = await datacubeClient.dataInsertion(dbName, collName, params.data)
                        console.log('Insert Response:', response);
                        break;

                    case 'update':
                        // response = await datacubeClient.updateData(dbName, collName, params.query, params.updateData);
                        response = await datacubeClient.dataUpdate(dbName, collName, params.query, params.updateData);

                        console.log('Update Response:', response);
                        break;

                    case 'delete':
                        // response = await datacubeClient.deleteData(dbName, collName, params.query);
                        response = await datacubeClient.dataDelete(dbName, collName, params.query);
                        console.log('Delete Response:', response);
                        break;

                    case 'fetch':
                        // response = await datacubeClient.fetchData(dbName, collName, params.filters, params.limit, params.offset);

                        response = await datacubeClient.dataRetrieval(dbName, collName, params.filters, params.limit)
                        sendToKafka('place-details', response)

                        console.log('Fetch Response:', response);

                        break;
                    default:
                        console.log(`Unknown action: ${action}`);
                        break;
                }
            } catch (error) {
                console.error(`Error processing message: ${error.message}`, error);
            }
        }
    });

    console.log("Consumer successfully started");
}

startConsumer().catch(console.error);
// module.exports = startConsumer;

// export default startConsumer