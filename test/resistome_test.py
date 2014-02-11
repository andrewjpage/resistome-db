import sys, os
sys.path.append('../modules')
sys.path.append('..')

import manage_pickle, ena_metadata
from resistome import parse_args
import pytest

def test_add():
        args = ['-f', 'test/data/small_db.txt', '-d', 'resistome_testing', '-c', 'test/data/test.conf']
        opts = parse_args(args)
        manage_pickle.run('add', opts)
        
        assert os.path.exists('resistome_testing.db')
        
def test_update():
        args = ['-f', 'test/data/notes.txt', '-t', 'Notes', '-d', 'resistome_testing', '-c', 'test/data/test.conf']
        opts = parse_args(args)
        manage_pickle.run('update', opts)
        
        