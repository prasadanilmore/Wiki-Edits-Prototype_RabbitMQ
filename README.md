# Wikipedia Data Transformation & Analysis

## Introduction

This project is a prototype for a data transformation and analysis system for Wikipedia changes. It involves a producer that reads sample data and emits it at random intervals into a RabbitMQ queue. A consumer then reads this data from the queue, performs aggregations, and stores the results in a PostgreSQL database. The system aims to provide insights into current Wikipedia trends and historical changes.

## Project Overview

The project consists of the following components:

- A RabbitMQ container for message queuing.
- A producer container for generating and publishing Wikipedia data to the RabbitMQ queue.
- A consumer container for consuming data from the RabbitMQ queue, performing aggregations, and storing the results in a PostgreSQL database.

## Getting Started

### Prerequisites

Before running the project, ensure you have the following prerequisites installed:

- [Docker](https://www.docker.com/get-started) - for containerization.

### Setting Up Docker

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/prasadanilmore/wikipedia-data-analysis.git
   cd wikipedia-data-analysis
<<<<<<< HEAD

=======
  
>>>>>>> 24e514f88e62f1d56afe2c33533bc59b00617043
