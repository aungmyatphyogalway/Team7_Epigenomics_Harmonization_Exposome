#!/usr/bin/env python3
"""
download_and_melt_cptac2.py

Fetches all *.htseq_counts.txt.gz from the public CPTAC-2 bucket and writes
out a long-form TSV with columns:
  ensembl_id    value    sample_id
"""

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pandas as pd
import io
import sys

BUCKET   = 'gdc-cptac-2-phs000892-2-open'
EXT      = '.htseq_counts.txt.gz'
OUTPUT = 'cptac2_long_with_sample.tsv'


def list_htseq_keys(s3):
    """ 
    Yield every S3 key in BUCKET ending with EXT
    """
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith(EXT):
                yield key


def load_counts_from_s3(s3, key):
    """
    Read one gzipped HTSeq count file from S3 into a pandas Series.
    Index = ensemble gene ID; values = integer counts.
    """
    resp = s3.get_object(Bucket=BUCKET, Key=key)
    body = resp['Body'].read()
    df = pd.read_csv(
        io.BytesIO(body),
        sep='\t', header=None,
        names=['gene','count'],
        index_col='gene',
        compression='gzip'
    )
    return df['count']


def build_and_melt():
    """
    Downloads all samples, builds a wide DataFrame (genes×samples),
    then melts to long form and returns it.
    """
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    records = []

    for key in list_htseq_keys(s3):
        sample = key.split('/')[0]
        sys.stdout.write(f'▶ processing {sample}...\r')
        sys.stdout.flush()
        series = load_counts_from_s3(s3, key)
        for gene, count in series.items():
            records.append((gene, int(count), sample))

    df = pd.DataFrame(records, columns=['ensembl_id', 'value', 'sample_id'])
    return df


if __name__ == '__main__':
    print("Building long-form TSV…")
    df = build_and_melt()
    df.to_csv(OUTPUT, sep='\t', index=False)
    print(f"Wrote long-form TSV to {OUTPUT} ({df.shape[0]} rows)")