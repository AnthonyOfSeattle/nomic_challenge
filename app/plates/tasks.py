from celery import shared_task
from searches.models import Search, Result
from genomes.records import GenomeBank
from django.utils import timezone


@shared_task
def run_search(pk, sequence):
    """Search genomes for sequence and associate result with primary key"""

    # Update search
    search = Search.objects.get(pk=pk)
    search.status = Search.RUNNING
    search.save()

    # Simulated search process
    try:
        result_dict = GenomeBank().query_genomes(search.sequence)
        search.status = Search.COMPLETE

    except:
        search.status = Search.ERROR

    # Create and save result if successful
    if search.status == Search.COMPLETE:
        result = Result(search=search,
                        **result_dict)
        result.save()

    # Update search
    search.finished = timezone.now()
    search.save()

