from extract import connect_to_api, extract_json
from producer_setup import kafka_producer, topic
import time

FETCH_INTERVAL = 300  # Fetch new data every 5 minutes (300 seconds)

def main() -> None:
    """
    Main function that continuously fetches stock data, processes it, and sends it to Kafka.

    Runs in an infinite loop with a configurable interval between fetches.
    Designed to run inside a Docker container as a long-running service.

    Performs the following tasks per cycle:
    1. Fetches stock data using connect_to_api().
    2. Extracts and formats the relevant data using extract_json().
    3. Sends the processed stock data to a Kafka topic via kafka_producer().
    4. Waits for the configured interval before fetching again.
    """
    while True:
        try:
            # Fetch stock data from the API
            response = connect_to_api()

            # Extract and format the relevant stock data
            data = extract_json(response)

            # Set up the Kafka producer
            producer = kafka_producer()

            # Send each stock record to the Kafka topic
            for stock in data:
                result = {
                    'date': stock['date'],
                    'symbol': stock['symbol'],
                    'open': stock['open'],
                    'low': stock['low'],
                    'high': stock['high'],
                    'close': stock['close']
                }

                producer.send(topic, result)
                print(f'Data sent to {topic} topic')

                # Sleep to avoid overloading the Kafka broker
                time.sleep(2)

            # Flush and close the producer after sending all data
            producer.flush()
            producer.close()

            print(f'Cycle complete. Waiting {FETCH_INTERVAL} seconds before next fetch...')
            time.sleep(FETCH_INTERVAL)

        except Exception as e:
            print(f'Error occurred: {e}. Retrying in 60 seconds...')
            time.sleep(60)


if __name__ == '__main__':
    main()