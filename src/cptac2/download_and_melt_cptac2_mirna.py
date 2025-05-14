#!/usr/bin/env python3
"""
download_and_concat_cptac2_mirna.py

Streams all *.mirnaseq.mirnas.quantification.txt files directly from the CPTAC-2 S3 bucket,
concatenates them into a single long-form TSV with columns:
  miRNA_ID    read_count    reads_per_million_miRNA_mapped    cross-mapped    sample_id
"""

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pandas as pd
import io
import sys

BUCKET      = 'gdc-cptac-2-phs000892-2-open'
EXT_KEYWORD = 'mirnaseq.mirnas.quantification.txt'
OUTPUT    = 'cptac2_mirna_long_with_sample.tsv'


def list_mirna_keys(s3):
    """Yield every S3 key containing EXT_KEYWORD."""
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if EXT_KEYWORD in key:
                yield key


def load_mirna_from_s3(s3, key):
    """
    Read one miRNA quantification file from S3 into a pandas DataFrame.
    Columns expected: miRNA_ID, read_count, reads_per_million_miRNA_mapped, cross-mapped
    """
    resp = s3.get_object(Bucket=BUCKET, Key=key)
    raw = resp['Body'].read().decode('utf-8')
    df = pd.read_csv(
        io.StringIO(raw),
        sep='\t',
        header=0,
        names=["miRNA_ID","read_count","reads_per_million_miRNA_mapped","cross-mapped"],
        dtype={"cross-mapped": str}
    )
    return df


def concat_mirna_stream():
    """
    Stream all miRNA files: read each into DataFrame, add sample_id, collect, concat.
    """
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    records = []
    keys = list(list_mirna_keys(s3))
    print(f"Found {len(keys)} miRNA files to process.")

    for key in keys:
        sample_id = key.split('/')[0]
        sys.stdout.write(f"▶ streaming {sample_id}...\r")
        sys.stdout.flush()
        df = load_mirna_from_s3(s3, key)
        df['sample_id'] = sample_id
        records.append(df)

    if records:
        df = pd.concat(records, ignore_index=True)
    else:
        df = pd.DataFrame(columns=[
            "miRNA_ID","read_count",
            "reads_per_million_miRNA_mapped","cross-mapped","sample_id"
        ])
    return df


if __name__ == '__main__':
    print("Concatenating miRNA quantification files into long-form TSV…")
    df = concat_mirna_stream()
    df.to_csv(OUTPUT, sep='\t', index=False)
    print(f"Wrote '{OUTPUT}' with {df.shape[0]} rows and {df.shape[1]} columns.")