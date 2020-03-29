import os, uuid
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
try:
    print("Azure Queue storage v12 - Python quickstart sample")
    # Quick start code goes here
    # Create a unique name for the queue
    queue_name = "quickstartqueues-" + str(uuid.uuid4())
    print("Creating queue: " + queue_name)
    # Instantiate a QueueClient which will be
    # used to create and manipulate the queue
    queue_client = QueueClient.from_connection_string(connect_str, "xvy")
    print("Creating queueszdfcsezfc: " )
    # Create the queue
    # queue_client.create_queue()
    queue_client.send_message(u"I'm using queues!")


    queue_client.send_me
except Exception as ex:
    print('Exception:')
    print(ex)