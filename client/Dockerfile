# Frontend Dockerfile for Node.js
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY client/package*.json ./
RUN npm install

# Copy the rest of the application
COPY client/ .

# Expose port if needed (optional but helpful)
EXPOSE 3000

# Start the frontend app
CMD ["npm", "run" , "dev"]
