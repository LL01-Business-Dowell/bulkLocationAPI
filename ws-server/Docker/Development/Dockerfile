# Specify the base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Suppress non-critical warnings
ENV NODE_NO_WARNINGS=1

# Copy package.json and package-lock.json
COPY package*.json ./

# Clear npm cache and install dependencies
# - `--legacy-peer-deps`: Allows installation despite peer dependency conflicts
# - `--loglevel=error`: Reduces verbosity to suppress non-critical warnings
RUN npm cache clean --force && npm install --legacy-peer-deps --loglevel=error

# Copy the rest of the code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Start the application
CMD ["npm", "run", "dev"]