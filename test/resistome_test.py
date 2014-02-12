import sys, os
sys.path.append(os.path.realpath('./modules'))
sys.path.append(os.path.realpath('.'))

from resistome import parse_args
import manage_pickle, ena_metadata
import pytest, filecmp, tempfile, shutil

# create temp dir and write config pointing to it
tmpdir = tempfile.mkdtemp(dir=os.getcwd())
confpath = "%s/test.conf" % tmpdir
conf = open(confpath, 'w')
conf.write("db_location\t%s\n" % tmpdir)
conf.close()

base_args = [ '-d', 'resistome_testing', '-c', confpath]

def test_add():
        args = ['-f', 'test/data/small_db.txt'] + base_args
        opts = parse_args(args)
        manage_pickle.run('add', opts)
        
        assert os.path.exists("%s/resistome_testing.db" % tmpdir)
        
def test_save():
        args = ['-f', "%s/test.csv" % tmpdir]  + base_args
        opts = parse_args(args)
        manage_pickle.run('save', opts)
        
        assert filecmp.cmp("%s/test.csv" % tmpdir, 'test/data/exp.csv')
        
def test_update():
        args = ['-f', 'test/data/notes.txt', '-t', 'Notes']  + base_args
        opts = parse_args(args)
        manage_pickle.run('update', opts)
        
        args = ['-f', "%s/updated.csv" % tmpdir]  + base_args
        opts = parse_args(args)
        manage_pickle.run('save', opts)
        
        assert filecmp.cmp("%s/updated.csv" % tmpdir, 'test/data/exp_updated.csv')

def test_single_acc_query():
        args = ['-q', 'CP000356', '-o', "%s/query_s.csv" % tmpdir]  + base_args
        opts = parse_args(args)
        manage_pickle.run('query', opts)
        
        assert filecmp.cmp("%s/query_s.csv" % tmpdir, 'test/data/query_s.exp')
        
def test_file_acc_query():
        args = ['-f', 'test/data/q.txt', '-o', "%s/query_f.csv" % tmpdir]  + base_args
        opts = parse_args(args)
        manage_pickle.run('query', opts)
        
        assert filecmp.cmp("%s/query_f.csv" % tmpdir, 'test/data/query_f.exp')
        
def test_single_other_query():
        args = ['-q', 'linear', '-t', 'Topology', '-o', "%s/query_o.csv" % tmpdir]  + base_args
        opts = parse_args(args)
        manage_pickle.run('query', opts)
        
        assert filecmp.cmp("%s/query_o.csv" % tmpdir, 'test/data/query_o.exp')
        
        cleanup()       
        
def test_metadata():
        acc = 'AJ511268'
        exp = {
	    'Molecule Type': 'genomic DNA', 
	    'Topology': 'linear',
	    'Organism': 'Pseudomonas aeruginosa', 
	    'Taxonomy': 'Bacteria; Proteobacteria; Gammaproteobacteria; Pseudomonadales; Pseudomonadaceae; Pseudomonas', 
	    'Taxon ID': '287', 
	    'Strain': '',
	    'Description': 'Pseudomonas aeruginosa partial type 1 integron In182', 
	    'Keywords': 'aac(3)-Ic gene; aminoglycoside acetyltransferase; blaVIM-2 gene; cmlA7 gene; CMLA7 protein; DNA integrase; integron; intI1 gene; qacEdelta1 gene; QacEdelta1 multidrug exporter; VIM-2 metallo-beta-lactamase', 
	    'Reference Location': 'Antimicrob. Agents Chemother. 47(5):1746-1748(2003).',
	    'PubMed ID': '12709352', 
	    'Notes': '', 
	    'URL': 'http://www.ebi.ac.uk/ena/data/view/AJ511268', 
	    'Sequence': '',
	    'First Release': '2003-04-24', 
	    'Last Updated': '2005-04-15'
	}
	
	got = ena_metadata.get_metadata(acc)
	
	assert got == exp

def cleanup():	
        shutil.rmtree(tmpdir)