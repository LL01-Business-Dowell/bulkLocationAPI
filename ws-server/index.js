const WebSocket = require('ws');
const { Kafka } = require('kafkajs');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

// const { MongoClient } = require('mongodb');

// --- Configuration ---
const PORT = 8080;
// const MONGODB_URI = 'mongodb://localhost:27017/';
// const DATABASE_NAME = 'your_database_name';
const NEARBY_PLACES_API = 'http://django-api-server:8001/get-local-nearby-v3/'; // Replace with your actual API
const PLACE_DETAILS_API = 'http://django-api-server:8001/get-details-list-stage1/'; // Replace with your actual API
const STORAGE_ENDPOINT = 'https://your-storage-endpoint.com/places'; // Replace with your actual endpoint
const KAFKA_BROKER = 'kafka:9092'; // Kafka broker address

// --- Kafka Setup ---
const kafka = new Kafka({
    clientId: 'location-service',
    brokers: [KAFKA_BROKER]
});

const producer = kafka.producer();
// const consumer = kafka.consumer({ groupId: 'receice-location-group' });

// --- MongoDB Setup ---
let db, placesCollection;

// async function initializeMongo() {
//     const mongoClient = new MongoClient(MONGODB_URI);
//     await mongoClient.connect();
//     db = mongoClient.db(DATABASE_NAME);
//     placesCollection = db.collection('places');
//     console.log("Connected to MongoDB");
// }

// --- API Helpers ---
async function fetchNearbyPlaces(lat, lng, radius1, radius2, query_string, limit) {
    try {
        // const response = await axios.get(`${NEARBY_PLACES_API}?lat=${lat}&lng=${lng}`);
        // return response.data.results.map(result => result.place_id);
        const response = await axios.post(`${NEARBY_PLACES_API}`,
            {
                radius1: radius1,
                radius2: radius2,
                center_lat: lat,
                center_lon: lng,
                query_string: query_string,
                limit: limit,
                api_key: "api_key"
            }

        );

        // return response.data.results.map(result => result.place_id_list);
        return response.data.place_id_list
    } catch (error) {
        console.error('Error fetching nearby places:', error);
        throw new Error(`Failed to fetch nearby places: ${error.message}`);
    }
}

async function fetchPlaceDetails(placeId) {
    try {
        // const response = await axios.get(`${PLACE_DETAILS_API}?place_id=${placeId}`);
        const response = await axios.post(`${PLACE_DETAILS_API}`,
            {
                place_id_list: placeId,
                center_loc: "",
                api_key: "api_key"
            }

        );
        return response.data;
    } catch (error) {
        console.error('Error fetching place details:', error);
        throw new Error(`Failed to fetch place details: ${error.message}`);
    }
}

async function storePlaceDetails(placeDetails) {
    try {
        const response = await axios.post(STORAGE_ENDPOINT, placeDetails);
        return response.data;
    } catch (error) {
        console.error('Error storing place details:', error);
        throw new Error(`Failed to store place details: ${error.message}`);
    }
}

// --- Kafka Producers and Consumers ---
// Producer
async function sendToKafka(topic, message) {
    await producer.connect();
    await producer.send({
        topic,
        messages: [{ value: JSON.stringify(message) }],
    });
    await producer.disconnect();
}

// Consumer for locations
async function consumeLocationMessages() {
    await consumer.subscribe({ topic: 'nearby-places' });
    await consumer.connect();

    await consumer.run({
        eachMessage: async ({ message }) => {
            const { lat, lng } = JSON.parse(message.value);
            const placeIds = await fetchNearbyPlaces(lat, lng);
            for (const placeId of placeIds) {
                await sendToKafka('place-details', { placeId });
            }
        },
    });
}

// Consumer for place details
async function consumePlaceDetailsMessages(consumer, ws) {
    await consumer.subscribe({ topic: 'place-details' });
    await consumer.connect();

    await consumer.run({
        eachMessage: async ({ message }) => {
            const rawMessage = message.value.toString();
            const msg = JSON.parse(rawMessage);

            ws.send(JSON.stringify({ status: 'success', message: "locations fetched successfully", data: msg.data }));
        },
    });
}

// --- WebSocket Server ---
const server = new WebSocket.Server({ port: PORT });

server.on('connection', (ws) => {
    console.log('Client connected');
    // ws.send(`Echo: Hi welcome to server`);

    ws.on('message', async (message) => {
        console.log(`Received: ${message}`);
        try {
            const data = JSON.parse(message);
            if (data && data.type && data.payload) {
                const { type, payload, extra_info } = data;
                const myID = uuidv4();
                switch (type) {
                    case "INSERT":
                        if (!Array.isArray(payload)) {
                            return ws.send(JSON.stringify({ status: "error", message: "Payload must be an array of lat, lng" }));
                        }
                        for (const { radius1, radius2, center_lat, center_lon, query_string, limit } of payload) {
                            try {
                                const placeIds = await fetchNearbyPlaces(center_lat, center_lon, radius1, radius2, query_string, limit);
                                // for (const placeId of placeIds) {
                                const placeDetails = await fetchPlaceDetails(placeIds);

                                placeDetails.scrape_id = myID
                                placeDetails.extra_info = extra_info
                                const message = {
                                    action: 'insert',
                                    dbName: 'bulklocations1',
                                    collName: 'collection_1',
                                    data: placeDetails
                                }
                                //  const response = await storePlaceDetails(placeDetails);
                                await sendToKafka('topic_1', message);


                                ws.send(JSON.stringify({ status: 'sent', message: `Data sent for storage with id: ${myID}` }));

                                // console.log(`Stored details for ${placeId}:`, response);
                                // }
                            }
                            catch (error) {
                                console.error('Error processing location:', error);
                                ws.send(JSON.stringify({ status: 'error', message: `Error processing location: ${error.message}` }));
                            }
                        }
                        // for (const { lat, lng } of payload) {
                        //     await sendToKafka('topic_1', { lat, lng });
                        // }
                        ws.send(JSON.stringify({ status: 'ok', message: 'Location data received and jobs enqueued' }));
                        break;
                    case "READ":
                        // implement read if needed
                        filter = {}

                        if (payload.hasOwnProperty('scrape_id')) {
                            filter.scrape_id = payload.scrape_id;
                        }
                        if (Object.keys(extra_info).length !== 0) {
                            console.log("lenght not equal to zero")
                            filter.extra_info = extra_info
                        }
                        const message = {
                            action: 'fetch',
                            dbName: 'bulklocations1',
                            collName: 'collection_1',
                            filters: filter
                        }
                        //  const response = await storePlaceDetails(placeDetails);
                        await sendToKafka('topic_1', message);
                        const consumer = kafka.consumer({ groupId: 'change-location-group' });
                        consumePlaceDetailsMessages(consumer, ws)


                        // ws.send(JSON.stringify({ status: 'sent', message: `Data sent for storage with id: ${myID}` }));


                        ws.send(JSON.stringify({ status: "ok", message: "Consumer implemented" }));
                        break;
                    case "UPDATE":
                        // implement update if needed
                        ws.send(JSON.stringify({ status: "ok", message: "Update not implemented" }));
                        break;
                    case "DELETE":
                        // implement delete if needed
                        ws.send(JSON.stringify({ status: "ok", message: "Delete not implemented" }));
                        break;
                    default:
                        ws.send(JSON.stringify({ status: "error", message: "Invalid operation type" }));
                        break;
                }
            } else {
                ws.send(JSON.stringify({ status: "error", message: "Invalid request format" }));
            }
        } catch (error) {
            console.error("Error processing message:", error);
            ws.send(JSON.stringify({ status: 'error', message: 'Error processing message, ensure valid JSON' }));
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

// --- Start Server ---
async function startServer() {
    // await initializeMongo();
    // await consumer.connect();
    // await consumer.subscribe({ topics: ['locations', 'place-details'] });
    // await consumeLocationMessages();
    // await consumePlaceDetailsMessages();
    console.log(`WebSocket server is running on ws://localhost:${PORT}`);
}
startServer();
