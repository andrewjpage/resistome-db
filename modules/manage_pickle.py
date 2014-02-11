import sys, os, glob, re
import cPickle as cp
from ena_metadata import get_metadata
headers = ['Accession No', 'Gene Name', 'Resistance', 'Molecule Type', 
         'Topology', 'Organism', 'Taxonomy', 'Sequence',
         'Taxon ID', 'Strain', 'Description', 'Keywords', 'Reference Location',
         'PubMed ID', 'Notes', 'URL', 'First Release', 'Last Updated']
         
database = []
database_name = ''
db_loc = ''
         
def run(mode, opts):
        global database, database_name, db_loc
        db_loc = read_config(opts.config)
        
        if mode == "avail":
                show_dbs()
                die("")
        
        
        if opts.database is None:
                print "Please provide the name of the database (-d)"
                sys.exit(2)
        else:
                dbname = "%s.db" % opts.database
                try:
                        database = cp.load( open("%s/%s" % (db_loc, dbname), 'rb') )
                except IOError:
                        if mode == 'add':
                                database = []
                        else:
                                print "Database '%s' not found" % opts.database
                                show_dbs()
                                sys.exit(2)
                                
                database_name = dbname
        
        if mode == "add":
                add_info(opts)
        elif mode == "query":
                search(opts)
        elif mode == "update":
                update_info(opts)
        elif mode == "save":
                write_csv(opts)
        elif mode == "test":
                initiate_test_sequence(opts)
    
def initiate_test_sequence(opt):
        data = get_metadata(opt.query)
        print data    

def add_info(opts):
        global database
        
        # check arguments
        if opts.file is None:
                die("Please provide an input file with the -f option")
        elif not os.path.exists(opts.file):
                die("Cannot find file '%s'" % opts.file)
        
        data = parse_flatfile(opts.file)
        for c,d in enumerate(data):
                meta = get_metadata(d['Accession No'])
                data[c] = dict(d.items() + meta.items())

                #print data[c]
                database.append(data[c])
                
        # save updated version of DB to pickle
        cp.dump( database, open("%s/%s" % (db_loc, database_name), 'wb') )     
        
        
def update_info(args):
        global database
        
        [info_file, term] = update_args(args)
        check_term(term)
        
        # parse info file
        info = {}
        for line in open(info_file):
                cols = line.rstrip().split("\t")
                info[cols[0]] = cols[1]
                
        # add notes to database
        for c,d in enumerate(database):
                if d['Accession No'] in info.keys():
                        database[c][term] += "%s; " % info[d['Accession No']] 
                        
        # save updated version of DB to pickle
        cp.dump( database, open("%s/%s" % (db_loc, database_name), 'wb') )
        
                
def write_csv(opts):
        if opts.file is None:
                die("Please provide an output file name (-f)")
                
        out = open(opts.file, 'w')
        
        # write header
        out.write("%s\n" % "\t".join(headers))
        
        # write data
        for d in database:
                line = print_line(d)
                out.write("%s\n" % line)
    
        out.close()
        
def print_line(d):
        line = []
        for h in headers:
                if h == 'Resistance':
                        line.append(", ".join(d[h]))
                else:
                        if d[h] == '':
                                line.append('NA')
                        else:
                                line.append(d[h])
                 
        return "\t".join(line)

def search(args):
        [search_ids, search_term] = search_args(args)
           
        check_term(search_term)
                
        # if valid, return all matches
        print "\t".join(headers)
        for d in database:
                for sid in search_ids:
                        if sid in d[search_term]:
                                print print_line(d)
   
def check_term(search_term):
        # check valid search term
        try:
                database[0][search_term]
        except KeyError:
                print "Invalid info type '%s'. Please use one of the following:" % search_term
                print "\n".join(["- %s" % x for x in headers])
                sys.exit(2)
          
def parse_flatfile(db_file):
    data = []
    for line in open(db_file):
        cols = line.split()

        # split name from acc#
        name_acc = cols[0].split('_')
        acc = name_acc.pop()
        name = "_".join(name_acc)

        # split resistant antibiotics
        try:
            res = cols[1].split('_')
        except IndexError:
            res = []

        data.append({'Gene Name': name, 'Accession No': acc, 'Resistance': res})

    return data
    
def show_dbs():
        dbs = glob.iglob("%s/*.db" % db_loc)
        dbs = [re.sub("%s/" % db_loc, "", x) for x in dbs]
        dbs = [re.sub("\.db", "", x) for x in dbs]
        
        print "Available databases:"
        print "\n".join(dbs)
        
                          
def search_args(args):
        # check valid args
        if args.query is None and args.file is None:
                die("Please provide a -q or -f option!\n")

        if args.file is not None:
                if not os.path.exists(args.file):
                        die("File '%s' does not exist" % args.file)

        # get search IDs
        if args.query:
                search_id = [args.query]
        elif args.file:
                search_id = [x.rstrip() for x in open(args.file)]

        return [search_id, args.type]


def update_args(args):
        if args.file is None:
                die("Please provide an input file (-f option)")
        else:
                info_file = args.file

        return [info_file, args.type]
              
def read_config(confile):
        for key,val in [x.split("\t") for x in open(confile)]:
                if key == 'db_location':
                        return val
        
                
def die(message):
        print message
        sys.exit(2)