import os
import json
from glob import glob
from Bio import Entrez, SeqIO


class Genome:
    """Custom Genbank file reader with CDS iteration."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.name = os.path.splitext(
                      os.path.basename(file_path)
                    )[0]

    def iter_coding_sequences(self):
        """Yield coding sequences from Genbank file."""

        gb_record = SeqIO.read(open(self.file_path), 'genbank')
        for gb_feature in gb_record.features:
            if gb_feature.type == 'CDS':
                protein = gb_feature.qualifiers['protein_id'][0]
                sequence = gb_feature.extract(gb_record.seq)

                yield (protein, sequence)


class GenomeBank:
    """Class for building and query a cache of Genbank files."""

    def __init__(self):
        self.cache_path = self._get_cache_path()

    def _get_cache_path(self):
        """Returns the path of the default cache, which may be relative."""

        default_cache = os.path.join(os.path.expanduser('~'), '.seqsleuth.cache')
        return os.environ.get('GENOME_BANK_PATH', default_cache)

    def _retrieve_genome(self, genome):
        """Retrieves and stores one Genbank file from the NCBI."""

        gb_file = os.path.join(self.cache_path, genome + '.gbk')
        if not os.path.exists(gb_file):
            print('Genome file for {} does not exist. Downloading now...'.format(genome))

            # get entrez id
            entrez_search = Entrez.esearch(db='nuccore', term=genome, retmode='json')
            entrez_search = json.load(entrez_search)
            entrez_id = entrez_search['esearchresult']['idlist'][0]

            # get genbank file
            src = Entrez.efetch(db='nuccore', id=entrez_id, rettype='gb', retmode='text')
            dest = open(gb_file, 'w')
            for line in src:
                dest.write(line)

    def initialize_bank(self, genome_list):
        """Initialize the cache with all genomes in list."""

        try:
            os.makedirs(self.cache_path)
        except FileExistsError:
            if not os.path.isdir(self.cache_path):
                raise

        for genome in genome_list:
            self._retrieve_genome(genome)

    def get_genomes(self):
        """Get genomes from cache."""

        genome_paths = glob(os.path.join(self.cache_path, '*.gbk'))
        return [Genome(p) for p in genome_paths]

    def query_genomes(self, query):
        """Walk through coding sequences in cache and search for a query sequence."""

        for genome in self.get_genomes():
            for protein, sequence in genome.iter_coding_sequences():
                start = sequence.find(query)
                if start > -1:
                    return {'genome'  : genome.name,
                            'protein' : protein,
                            'start'   : start + 1,
                            'end'     : start + len(query)}

        return {'genome'  : 'NOT FOUND',
                'protein' : 'NOT FOUND',
                'start'   : -1,
                'end'     : -1}

