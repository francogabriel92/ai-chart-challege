FROM node:22-alpine

WORKDIR /app

# Copy source code
COPY . .

# Clean install to avoid dependency conflicts
RUN rm -rf node_modules && npm install

# Expose port 5173
EXPOSE 5173

# Start development server with host binding
CMD ["npm", "run", "dev"]