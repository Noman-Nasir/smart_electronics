"""This module is responsible for reading device information from the csv file and adding it to the database"""
import csv
import logging
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from devices.models import Device


def get_devices_from_csv(devices_csv):
    """Reads the given csv file and returns Devices to be added.

    Reads csv file and verifies each device in the file to be a valid
    Device. Reads column names from csv and zips them with each device
    to create a dict. Dict is first verified and then converted to
    an Device object.

    Arguments:
        devices_csv (TextIO): device fields as key value pairs
    Returns:
        devices_to_add (list<Device>): List of device read from csv file
    """

    logging.basicConfig(filename='device.log', filemode='a', level=logging.DEBUG)

    logging.info(f'Starting to add device from csv file at: {datetime.now()}')

    devices_csv_reader = csv.reader(devices_csv, delimiter=',')
    column_names = None
    devices_to_add = []
    for lineno, row in enumerate(devices_csv_reader):
        if lineno == 0:
            column_names = row
        else:

            device = dict(zip(column_names, row))

            try:
                device_to_add = Device(**device)
                device_to_add.full_clean()
            except (ValidationError, TypeError) as error:
                logging.error(f'Device with row number {lineno} couldn\'t be added. Failed with error: {error}')
                continue

            logging.info(f'Device with row number: {lineno} is clean.')

            devices_to_add.append(device_to_add)
    return devices_to_add


class Command(BaseCommand):
    """Class to add device from csv file to database."""
    help = 'Adds Devices from the given csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', nargs=1, type=str)

    def handle(self, *args, **options):
        """Adds device from csv file to database using bulk_create"""
        devices_csv_path = options['csv_file_path'][0]
        try:
            with open(devices_csv_path) as csv_file:
                devices_to_add = get_devices_from_csv(csv_file)

        except FileNotFoundError:
            raise CommandError('File "%s" does not exist' % devices_csv_path)

        Device.objects.bulk_create(devices_to_add)
        logging.info(f'Devices Added to the database at: {datetime.now()}')
