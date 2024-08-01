import os
import sys
from genomes.records import GenomeBank
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Builds cache of genomes'

    def handle(self, *args, **options):
        GENOME_LIST = os.environ.get('GENOME_LIST', '').split()
        GenomeBank().initialize_bank(GENOME_LIST)
