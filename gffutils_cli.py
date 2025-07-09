#!/usr/bin/env python

import os
import gffutils
import gffutils.helpers as helpers
from gffutils.exceptions import FeatureNotFoundError
import gffutils.gffwriter as gffwriter
import argh
from argcomplete.completers import EnvironCompleter
from argh import arg
import sys

# D.R.Y.
db_help = '''Database to use.  If a GFF or GTF file is provided instead for
this argument, a database will be created for you.  This can take some time
(several minutes), so it's best to create one ahead of time.'''

@arg('filename', help='GFF or GTF file to use')
@arg('--output', help='''Database to create.  Default is to append ".db" to the
     end of the input filename''')
@arg('--force', help='''Overwrite an existing database''')
@arg('--quiet', help='''Suppress the reporting of timing information when
     creating the database''')
@arg('--merge', help='''Merge strategy to be used if if duplicate IDs are
     found.''')
@arg('--disable-infer-genes', help='''Disable inferring of gene
     extents for GTF files. Use this if your GTF file already has "gene"
     featuretypes''')
@arg('--disable-infer-transcripts', help='''Disable inferring of transcript
     extents for GTF files. Use this if your GTF file already has "transcript"
     featuretypes''')
def create(filename, output=None, force=False, quiet=False, merge="merge",
           disable_infer_genes=False, disable_infer_transcripts=False):
    """
    Create a database.
    """
    verbose = not quiet
    if output is None:
        output = filename + '.db'
    gffutils.create_db(filename, output,
                       force=force,
                       verbose=verbose,
                       merge_strategy=merge,
                       disable_infer_genes=disable_infer_genes,
                       disable_infer_transcripts=disable_infer_transcripts)


@arg('db', help=db_help)
@arg('ids', help='Comma-separated list of IDs to fetch, or a file with one ID per line')
def fetch(db, ids):
    """
    Fetch IDs from the database.

    `ids` can be:
    - a comma-separated list like "gene1,gene2"
    - or a file path with one ID per line
    """
    if not os.path.isfile(db):
        raise Exception("Cannot fetch: %s does not exist." % db)

    gff_db = None
    if not helpers.is_gff_db(db):
        gff_db = helpers.get_gff_db(db)
    else:
        gff_db = db
    gff_db = gffutils.FeatureDB(gff_db)

    if os.path.isfile(ids):
        with open(ids) as f:
            id_list = [line.strip() for line in f if line.strip()]
    else:
        id_list = ids.split(',')

    for i in id_list:
        print(i)
        try:
            yield gff_db[i]
        except FeatureNotFoundError:
            print("%s not found" % i, file=sys.stderr)

@arg('db', help=db_help)
@arg('bed', help='BED3 file with regions to query')
def region(db, bed, feature_type=None):
    """
    Query GFF DB for features overlapping regions from a BED3 file.
    """
    if not os.path.isfile(db):
        raise Exception(f"Cannot open db: {db}")
    if not os.path.isfile(bed):
        raise Exception(f"Cannot open BED file: {bed}")

    if not helpers.is_gff_db(db):
        db = helpers.get_gff_db(db)
    gff_db = gffutils.FeatureDB(db)

    with open(bed) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            chrom, start, end = line.strip().split()[:3]
            start = int(start) + 1
            end = int(end)

            results = gff_db.region(region=(chrom, start, end), completely_within=False)

            for feat in results:
                yield feat

if __name__ == "__main__":
    argh.dispatch_commands([
        fetch,
        region,
        create,
#        search,
    ])
