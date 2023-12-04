FROM golang:1.21.4

# Set the working directory in the container
WORKDIR /users

# Copy the local package files to the container's workspace
COPY . .

# Build the Go application
RUN go build -o users

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable
CMD ["./users"]