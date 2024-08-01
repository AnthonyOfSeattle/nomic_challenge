from django.test import TestCase

import os
import tempfile
from genomes.records import *


class GenomeBankTests(TestCase):

    def test_genome_bank_gets_cache(self):
        """GenomeBank finds its cache."""
        env_save = os.environ.get('GENOME_BANK_PATH', '')

        # bank sets default cache
        os.environ.pop('GENOME_BANK_PATH', None)
        default_path = os.path.join(os.path.expanduser('~'), '.seqsleuth.cache')
        self.assertEqual(GenomeBank().cache_path, default_path)

        # bank gets cache from os
        test_path = '.test.cache'
        os.environ['GENOME_BANK_PATH'] = test_path
        self.assertEqual(GenomeBank().cache_path, test_path)

        # reset
        os.environ['GENOME_BANK_PATH'] = env_save

    def test_genome_bank_initializes(self):
        """GenomeBank initializes with Genbank files"""
        env_save = os.environ.get('GENOME_BANK_PATH', '')

        with tempfile.TemporaryDirectory() as temp_path:
            os.environ['GENOME_BANK_PATH'] = temp_path

            bank = GenomeBank()
            # bank does not fail but adds no files
            bank.initialize_bank([])
            self.assertEqual(len(os.listdir(temp_path)), 0)
            self.assertEqual(len(bank.get_genomes()), 0)

            # bank adds file
            bank.initialize_bank(['NC_000852'])
            self.assertEqual(len(os.listdir(temp_path)), 1)
            self.assertEqual(len(bank.get_genomes()), 1)

            # bank adds another file but does not delete
            GenomeBank().initialize_bank(['NC_007346'])
            self.assertEqual(len(os.listdir(temp_path)), 2)
            self.assertEqual(len(bank.get_genomes()), 2)

        # reset
        os.environ['GENOME_BANK_PATH'] = env_save

    def test_genome_iterates_through_coding_sequences(self):
        """Genome iterates through all coding sequences"""
        env_save = os.environ.get('GENOME_BANK_PATH', '')

        with tempfile.TemporaryDirectory() as temp_path:
            os.environ['GENOME_BANK_PATH'] = temp_path

            bank = GenomeBank()
            bank.initialize_bank(['NC_000852'])
            genome = bank.get_genomes()[0]

            # number of proteins should match expected
            protein_list = [protein for protein, sequence in genome.iter_coding_sequences()]
            self.assertEqual(len(protein_list), 802)

        # reset
        os.environ['GENOME_BANK_PATH'] = env_save

    def test_genome_bank_performs_queries(self):
        """GenomeBank returns first protein matching query"""
        env_save = os.environ.get('GENOME_BANK_PATH', '')

        with tempfile.TemporaryDirectory() as temp_path:
            os.environ['GENOME_BANK_PATH'] = temp_path

            bank = GenomeBank()
            bank.initialize_bank(['NC_000852'])

            # a short sequence will match many
            # but only the first matters
            seq = 'ATG'
            result = bank.query_genomes(seq)
            truth = {'genome'  : 'NC_000852',
                     'protein' : 'NP_048349.1',
                     'start'   : 1,
                     'end'     : 3}
            self.assertEqual(result, truth)

            # a specific sequence should return correctly
            seq = 'CCTTTTCTCTCGAGCGGAGGGAAAACGGAA'
            result = bank.query_genomes(seq)
            truth = {'genome'  : 'NC_000852',
                     'protein' : 'NP_048806.1',
                     'start'   : 323,
                     'end'     : 352}
            self.assertEqual(result, truth)

            # a non-existent sequence returns NOT FOUND
            # there is no validation in the GenomeBank
            # so anything besides ATCG will return NOT FOUND
            seq = 'a'
            result = bank.query_genomes(seq)
            truth = {'genome'  : 'NOT FOUND',
                     'protein' : 'NOT FOUND',
                     'start'   : -1,
                     'end'     : -1}
            self.assertEqual(result, truth)

        # reset
        os.environ['GENOME_BANK_PATH'] = env_save
