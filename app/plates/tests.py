from django.test import TestCase

import os
import tempfile
import datetime
from searches.models import *
from searches.tasks import *
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone

class SearchTests(TestCase):

    def test_search_is_created(self):
        """Test that search is created"""

        # search must be associated with a session
        session = Session(session_key='key',
                          expire_date=timezone.now())
        session.save()

        # test creation
        search = Search(sequence='GATACA', session=session)
        search.save()

        # check values
        self.assertEqual(search.status, Search.SUBMITTED)
        self.assertEqual(search.session.session_key, 'key')
        self.assertIs(search.finished, None)

        # check runtime
        self.assertIs(search.get_runtime(), None)
        search.status = Search.COMPLETE
        search.finished = search.started + datetime.timedelta(days=1)
        self.assertEqual(search.get_runtime().days, 1)

    def test_search_is_run(self):
        """Test that a search is run regardless of whether genomes are present"""

        # search must be associated with a session
        session = Session(session_key='key',
                          expire_date=timezone.now())
        session.save()

        # create search
        search = Search(sequence='GATACA', session=session)
        search.save()

        # run search
        run_search(search.id, search.sequence)

        # check that search object populated correctly
        search = Search.objects.get(pk=search.id)
        self.assertEqual(search.status, search.COMPLETE)
        self.assertIsNot(search.finished, None)
        self.assertIsNot(search.get_runtime(), None)

    def test_search_runs_correctly(self):
        """Test that search returns correct results"""
        env_save = os.environ.get('GENOME_BANK_PATH', '')

        with tempfile.TemporaryDirectory() as temp_path:
            os.environ['GENOME_BANK_PATH'] = temp_path

            bank = GenomeBank()
            bank.initialize_bank(['NC_000852'])

            # search must be associated with a session
            session = Session(session_key='key',
                              expire_date=timezone.now())
            session.save()

            # a specific sequence should return correctly
            search = Search(sequence='CCTTTTCTCTCGAGCGGAGGGAAAACGGAA',
                            session=session)
            search.save()
            run_search(search.id, search.sequence)
            result = Result.objects.get(search__id = search.id)
            self.assertEqual(result.protein, 'NP_048806.1')
            self.assertEqual(result.start, 323)

            # a non-existent sequence returns NOT FOUND
            # there is no validation in the GenomeBank
            # so anything besides ATCG will return NOT FOUND
            search = Search(sequence='a',
                            session=session)
            search.save()
            run_search(search.id, search.sequence)
            result = Result.objects.get(search__id = search.id)
            self.assertEqual(result.protein, 'NOT FOUND')
            self.assertEqual(result.start, -1)

        # reset
        os.environ['GENOME_BANK_PATH'] = env_save


