# Wikipedia Data Transformation & Analysis

## Introduction

This project serves as a prototype demonstrating RabbitMQ's capabilities with a "direct" exchange type. It comprises two key components: a producer that emits sample data at random intervals (between 0 and 1 second) and a RabbitMQ consumer. The consumer processes this data, performing aggregations, including tracking the global and german number of edits per minuteas well as stores the data in PostgreSQL database.

## Project Overview

The project consists of the following components:

- A RabbitMQ container for message queuing.
- A producer container for generating and publishing Wikipedia data to the RabbitMQ queue.
- A consumer container for consuming data from the RabbitMQ queue, performing aggregations, and storing the results in a PostgreSQL database.

## Getting Started

### Prerequites
Before running the project, ensure you have the following prerequisites installed:

- [Docker](https://www.docker.com/get-started) - for containerization.

### Dependencies
- Python 3.7
- Docker
- RabbitMQ 3.8-rc-management
- Pika 1.1.0
- PostgreSQL (for data storage and analysis)
- pgAdmin (for monitoring)

## Run the Program

### Setting Up Docker

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/prasadanilmore/wikipedia-data-analysis.git
   cd wikipedia-data-analysis

### Build the Docker Images

2. Build the images from the docker-compose.yml file
    ```bash
    docker-compose build

### Running the Project

3. Start the Docker containers in background with this command:
    ```bash
    docker-compose up -d

This will start the RabbitMQ, producer, and consumer containers.

### Monitor the Containers and Logs

4. To view the logs of the producer and consumer containers:

    ```bash
    docker-compose logs -f producer
    docker-compose logs -f consumer

To access the RabbitMQ management dashboard, open your web browser and navigate to http://localhost:15672. Login with the default credentials (username: 'admin', password: '1234')

### Stopping the Containers:

To stop the containers, use the following command: ```docker-compose down
    ```

To remove and clean up the containers: ```docker-compose down -v --rmi all --remove-orphans
    ```

### Monitoring the PostgreSQL Database with pgAdmin

1. Access the pgAdmin web interface by opening your web browser and navigating to http://localhost:8080.

2. Log in to pgAdmin with the following default credentials:

    - Email/Username: admin@europace.com (You can change this during the setup.)
    - Password: 1234 (You can change this during the setup.)

3. Once logged in, follow these steps:

    - Select "Create > Server and Fill in the following details for the new server:

        - Name: Enter a name for your server (e.g., "PostgreSQL Server").
        - Host name/address: Use the name of the PostgreSQL service in your Docker network (e.g., postgres) or localhost.
        - Port: 5432
        - Maintenance database: europace_db (the name of your database).
        - Username: europace (the username you set during the setup).
        - Password: europace (the password you set during the setup).
        - Click "Save" to add the server.

4. Expand your server to access the databases, and you will find the wikipedia_data database.

5. You can use pgAdmin to write SQL queries, analyze data, and visualize results.
