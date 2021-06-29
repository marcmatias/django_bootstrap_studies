# create_data.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from contacts.models import Contact
from utils.progress_bar import progressbar

fake = Faker()


def gen_email(first_name: str, last_name: str):
    first_name = slugify(first_name)
    last_name = slugify(last_name)
    email = f'{first_name}{last_name}.@email.com'
    return email


def get_contact():
    first_name = fake.first_name()
    last_name = fake.first_name()
    email = gen_email(first_name, last_name)
    birthday = fake.date()
    data = dict(
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthday=birthday
    )
    return data


def create_contact():
    aux_list = []
    for _ in progressbar(range(350), 'Contact'):
        data = get_contact()
        obj = Contact(**data)
        aux_list.append(obj)
    Contact.objects.bulk_create(aux_list)


class Command(BaseCommand):
    help = 'Create data.'

    def handle(self, *args, **options):
        create_contact()
