import pika
import os
import pandas as pd
import time
import random
import json

# Read the RabbitMQ connection URL from the environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# Connect to RabbitMQ
connection = pika.BlockingConnection(url_params)
channel = connection.channel()

# Declare a new queue
# Durable flag is set to retain messages even between restarts
exchange_name = 'wikipedia_edits'
queue_name = 'edits_queue'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=queue_name, durable=True)

# Path to the Wikipedia data CSV file
csv_name = 'de_challenge_sample_data.csv'

# Read the CSV data and Dataset reduced to two important columns for further analysis
df = pd.read_csv(csv_name, usecols=["timestamp", "wiki"])


def publish_edits_to_queue(df):
    """
    Publish Wikipedia edits to the RabbitMQ queue.

    Args:
        df (pandas.DataFrame): DataFrame containing Wikipedia edits data.

    Returns:
        None
    """
    for index, row in df.iterrows():
        routing_key = "global"

        # Check if it's a German Wikipedia edit
        if row["wiki"] == "dewiki":
            routing_key = 'german'

        row_dict = row.to_dict()
        row_json = json.dumps(row_dict)

        # Publish the message to the RabbitMQ exchange
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key,
                              body=row_json, properties=pika.BasicProperties(delivery_mode=2))
        print("Produced the message")
        
        # Sleep for a random interval between 0 to 1 second
        time.sleep(random.uniform(0, 1))

# Publish Wikipedia edits to the RabbitMQ queue
publish_edits_to_queue(df)

# Close the channel and connection to avoid lingering messages
channel.close()
connection.close()
