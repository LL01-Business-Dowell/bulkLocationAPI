// const { axios } = require('axios');
import axios from 'axios';


class DatacubeApiClient {
    constructor(baseURL) {
        this.api = axios.create({
            baseURL,
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // Data CRUD Endpoints
    async fetchData(dbName, collName, filters = {}, limit = 50, offset = 0) {
        try {
            const response = await this.api.get('/api/crud/', {
                data: {
                    db_name: dbName,
                    coll_name: collName,
                    operation: 'fetch',
                    filters,
                    limit,
                    offset,
                },
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async insertData(dbName, collName, data) {
        try {
            const response = await this.api.post('/api/crud/', {
                db_name: dbName,
                coll_name: collName,
                operation: 'insert',
                data,
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async updateData(dbName, collName, query, updateData) {
        try {
            const response = await this.api.put('/api/crud/', {
                db_name: dbName,
                coll_name: collName,
                operation: 'update',
                query,
                update_data: updateData,
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    async deleteData(dbName, collName, query) {
        try {
            const response = await this.api.delete('/api/crud/', {
                data: {
                    db_name: dbName,
                    coll_name: collName,
                    operation: 'delete',
                    query,
                },
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // List Collections
    async listCollections(dbName) {
        try {
            const response = await this.api.get('/api/list_collections/', {
                data: {
                    db_name: dbName,
                },
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Add Collection
    async addCollection(dbName, collName) {
        try {
            const response = await this.api.post('/api/add_collection/', {
                db_name: dbName,
                coll_names: collName,
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    // Create Database
    async createDatabase(dbName, numCollections, collNames, numDocuments, numFields, fieldLabels) {
        try {
            const response = await this.api.post('/api/create_database/', {
                db_name: dbName,
                num_collections: numCollections,
                coll_names: collNames,
                num_documents: numDocuments,
                num_fields: numFields,
                field_labels: fieldLabels,
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }
}

// module.exports = DatacubeApiClient;
export default DatacubeApiClient;
