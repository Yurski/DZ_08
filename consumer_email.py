import pika
import os
from models import Contact

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f'Sending email to {contact.email}...')  # Заглушка для надсилання email
        contact.message_sent = True
        contact.save()
        print(f'Email sent to {contact.email}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq',
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_DEFAULT_USER'),
            password=os.getenv('RABBITMQ_DEFAULT_PASS')
        )
    ))
    channel = connection.channel()
    channel.queue_declare(queue='email')

    channel.basic_consume(queue='email', on_message_callback=callback)

    print('Waiting for messages.')
    channel.start_consuming()

if __name__ == '__main__':
    main()
