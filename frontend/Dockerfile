# Use node
FROM node:18

# Working directory inside container
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of project
COPY . .

# Vite needs this to be accessible outside container
EXPOSE 8000

# Run Vite server accessible to outside world
CMD ["npm", "run", "dev"]
