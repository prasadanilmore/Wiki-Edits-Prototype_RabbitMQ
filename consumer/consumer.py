import pika
import os
import json
import pandas as pd
from postgres_util import Postgres_DB

# Read the RabbitMQ connection URL from the environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# Connect to RabbitMQ
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

# Declare Direct Exchange
exchange_name = 'wikipedia_edits'
chan.exchange_declare(exchange=exchange_name, exchange_type='direct')

# Declare a new queue for each routing keys
# Durable flag is set to retain messages even between restarts
queue_name = 'edits_queue'
chan.queue_declare(queue=queue_name, durable=True)
chan.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='global')
chan.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='german')

# Initialize the PostgreSQL database connection
POSTGRES_DB = 'europace_db'
POSTGRES_USER = 'europace'
POSTGRES_PASSWORD = 'europace'
POSTGRES_HOST = 'database'  # Use the service name defined in docker-compose.yml
POSTGRES_PORT = 5432

postgres_db = Postgres_DB(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST, 
    port=POSTGRES_PORT
)

# Create the table in PostgreSQL database
postgres_db.create_table()

global_edits_per_minute = {}
german_edits_per_minute = {}


def receive_msg(ch, method, properties, body):
    """
    Receive and process a message from RabbitMQ.

    Args:
        ch: RabbitMQ channel.
        method: RabbitMQ method.
        properties: RabbitMQ properties.
        body: Message body.

    Returns:
        None
    """
    global global_edits_per_minute
    global german_edits_per_minute

    data = json.loads(body)
    # Convert the timestamp to a Pandas Timestamp object
    timestamp = pd.to_datetime(data['timestamp'], unit='s')
    
    # Floor the Timestamp to the nearest minute
    key = timestamp.floor('T')
    
    # Calculate the per-minute aggregations
    timestamp_str = key.strftime('%Y-%m-%d %H:%M:%S')
    if timestamp_str not in global_edits_per_minute:
        global_edits_per_minute[timestamp_str] = 0
    if timestamp_str not in german_edits_per_minute:
        german_edits_per_minute[timestamp_str] = 0

    global_edits_per_minute[timestamp_str] += 1 if data["wiki"] != "dewiki" else 0
    german_edits_per_minute[timestamp_str] += 1 if data["wiki"] == "dewiki" else 0

    # Store the per-minute aggregations in the database
    for minute, count in global_edits_per_minute.items():
        postgres_db.insert_data(minute, 'global', count)
    for minute, count in german_edits_per_minute.items():
        postgres_db.insert_data(minute, 'german', count)

    print('received msg : ', body.decode('utf-8'))
 
    # Acknowledge the message
    print('acking it')
    ch.basic_ack(delivery_tag=method.delivery_tag)


# to make sure the consumer receives only one message at a time
# next message is received only after acking the previous one
chan.basic_qos(prefetch_count=1)

# define the queue consumption
chan.basic_consume(queue=queue_name, on_message_callback=receive_msg)

# start consuming
print("Start Consuming")
chan.start_consuming()

# Closing the Database connection
print("Closing the Database connection")
postgres_db.close()