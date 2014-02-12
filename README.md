resistome-db
============

Pull metadata from EBI's ENA database for given accession numbers and save resistance status with the metadata.

Usage: resistome.py <mode> <inputs>

 Modes:
 add:    add data to database. Input files should take the format:
         aac_1_AJ628983 aminoglycoside
         aac_3_I_1_AJ877225 aminoglycoside
         aac_3_Ia_1_X15852 aminoglycoside
         i.e.
         gene_name_ACCNO123 resistance 

         -f|file         input file
         -d|database     name of database to add data to

         The update function will collect metadata from ENA based on the acc#
         and add it to the database

         Example:
         resistome.py add -f database.file.txt -d resistome1

 update: add additional information to entries. Input should take the format:
         ACCNO123        This is my note for accession ACCNO123
         ACCNO456        Here is another note

         -f|file       input file
         -t|type       type of info (Notes, Sequence, etc)
         -d|database   name of database
         
         Example:
         resistome.py update -f note_list.txt -t Notes -d resistome1

 query:  query information from the database. Input may be a search term or a
         file of search terms (one per line).
         Searches on accession number as default. 
         
         -q|query         search term
         -f|file          file of search terms
         -t|type          specify a different search field.
         -d|database      name of database
         -o|query-output  output file name
         
         Example:
         resistome.py query -q ACCNO123 -d resistome1
         resistome.py query -f file_of_accessions.txt -d resistome1
         resistome.py query -q aminoglycoside -t Resistance -d resistome1
         
         Note: for queries (or types) with more than one word, use "". Example:
         resistome.py query -q "genomic DNA" -t "Molecule Type" -d resistome1

 save:   save data to a CSV file.

         -f|file        CSV output file
         -d|database    name of database
         
         Example:
         resistome.py save -f output_db.csv -d resistome1

 avail:  list available databases
 
         Example:
         resistome.py avail
         
 help:   Show this help menu