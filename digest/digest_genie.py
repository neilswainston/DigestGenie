'''
(c) University of Liverpool 2019

All rights reserved.

@author: neilswainston
'''
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=wrong-import-order
import os
import shutil
import sys

import pandas as pd
from synbiochem.utils import ice_utils, dna_utils, seq_utils


def digest(url, username, password,
           ice_ids_filename,
           restricts, circular=True,
           dir_name='out'):
    '''Get ICE sequences.'''
    ice_client = ice_utils.ICEClient(url, username, password)
    ice_ids = _get_ice_ids(ice_ids_filename)

    id_digests = {ice_id: dna_utils.apply_restricts(
        ice_client.get_ice_entry(ice_id).get_dna(),
        restricts,
        circular)
        for ice_id in ice_ids}

    _mkdirs(dir_name)

    data = []

    for ice_id, digests in id_digests.items():
        for idx, dna in enumerate(digests):
            dig_id = '%s_%s' % (ice_id, idx)
            seq = dna['seq']
            seq_utils.write_fasta({dig_id: seq},
                                  os.path.join(dir_name, dig_id + '.fasta'))
            data.append([ice_id, idx + 1, len(dna), seq])

    # Write csv file:
    df = pd.DataFrame(data, columns=['ice_id', 'digest_idx', 'len', 'seq'])
    df.to_csv(os.path.join(dir_name, 'digests.csv'), index=False)

    # Get Genbank files for subsequent data analysis:
    for ice_id in ice_ids:
        gb_filename = os.path.join(dir_name, ice_id + '.gb')
        ice_client.get_genbank(ice_id, gb_filename)


def _get_ice_ids(ice_ids_filename):
    '''Get ICE ids.'''
    with open(ice_ids_filename, 'r') as ice_ids_file:
        return [line.strip() for line in ice_ids_file]


def _mkdirs(dir_name):
    '''Make directories.'''
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

    os.makedirs(dir_name)


def main(args):
    '''main method.'''
    url = args[0]
    username = args[1]
    password = args[2]
    ice_ids_filename = args[3]
    circular = bool(args[4])
    dir_name = args[5]
    restricts = args[6:]

    digest(url, username, password,
           ice_ids_filename,
           restricts, circular,
           dir_name)


if __name__ == '__main__':
    main(sys.argv[1:])
