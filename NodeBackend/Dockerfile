# Use official Node.js LTS image
FROM node:20-alpine

# Set working directory to app root
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the app
COPY . .

# Build the app
RUN npm run build

# Expose port (default NestJS port)
EXPOSE 3000

# Start the NestJS app
CMD ["npm", "run", "start:prod"]
