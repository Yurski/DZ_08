import pika
import os
from faker import Faker
from models import Contact
import random

fake = Faker()

def generate_fake_contact():
    return Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        preferred_contact_method=random.choice(['email', 'sms'])
    )

def send_to_queue(contact_id, method):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq',
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_DEFAULT_USER'),
            password=os.getenv('RABBITMQ_DEFAULT_PASS')
        )
    ))
    channel = connection.channel()
    channel.queue_declare(queue=method)
    channel.basic_publish(exchange='', routing_key=method, body=str(contact_id))
    connection.close()

def main():
    for _ in range(10):  # Генерація 10 контактів
        contact = generate_fake_contact()
        contact.save()
        queue_name = 'sms' if contact.preferred_contact_method == 'sms' else 'email'
        send_to_queue(contact.id, queue_name)

if __name__ == '__main__':
    main()
