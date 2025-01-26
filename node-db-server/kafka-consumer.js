// const { Kafka } = require('kafkajs');
// const { DatacubeApiClient } = require('./Datacube.js');
import { Kafka } from 'kafkajs';
import DatacubeApiClient from './Datacube.js';

async function startConsumer() {
    const kafka = new Kafka({
        clientId: 'consumer',
        brokers: ['kafka:9092']
    });

    const consumer = kafka.consumer({ groupId: 'group1', sessionTimeout: 30000, });
    await consumer.connect();
    await consumer.subscribe({ topic: 'test-topic', fromBeginning: true, config: { 'auto.offset.reset': 'earliest' } });

    // Instantiate the MongoApiClient with your API's base URL
    const datacubeClient = new DatacubeApiClient('https://datacube.uxlivinglab.online/'); // Update with actual base URL

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {


            try {
                const rawMessage = message.value.toString();
                const msg = JSON.parse(rawMessage);
                console.log(`Raw message received: ${rawMessage}`);
                console.log(`Received message: ${JSON.stringify(msg)}`);
                let response;
                const { action, dbName, collName, ...params } = msg;

                switch (action) {
                    case 'insert':
                        response = await datacubeClient.insertData(dbName, collName, params.data);
                        console.log('Insert Response:', response);
                        break;

                    case 'update':
                        response = await datacubeClient.updateData(dbName, collName, params.query, params.updateData);
                        console.log('Update Response:', response);
                        break;

                    case 'delete':
                        response = await datacubeClient.deleteData(dbName, collName, params.query);
                        console.log('Delete Response:', response);
                        break;

                    case 'fetch':
                        response = await datacubeClient.fetchData(dbName, collName, params.filters, params.limit, params.offset);
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

// startConsumer().catch(console.error);
// module.exports = startConsumer;

export default startConsumer