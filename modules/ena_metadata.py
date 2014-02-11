import urllib2, sys, re, getopt
import xml.etree.ElementTree as ET

def get_metadata(acc):
        meta = {
	    'Molecule Type': '', 'Topology': '',
	    'Organism': '', 'Taxonomy': '', 'Taxon ID': '', 'Strain': '',
	    'Description': '', 'Keywords': '', 'Reference Location': '',
	     'PubMed ID': '', 'Notes': '', 'URL': '', 'Sequence': '',
	     'First Release': '', 'Last Updated': ''
	}
    
        url = "http://www.ebi.ac.uk/ena/data/view/%s" % acc
        meta['URL'] = url
        url += "&display=xml"
        xml = ''
        try:
	    xml = urllib2.urlopen(url)
	except urllib2.URLError:
	    print "Error accessing %s" % url
	
	# parse
	root = ET.fromstringlist(xml.readlines())
	
	# check if valid
	if "entry is not found" in root.text:
	    return meta
	    
	    
	print acc
	
	# get interesting elements
	entry = root.find('entry')
	if entry is None:
	        return meta
	[meta['Molecule Type'], meta['Topology'], meta['Keywords'], meta['First Release'], meta['Last Updated']] = _entry_metadata(entry)
	
	description = entry.find('description')
	meta['Description'] = description.text if description is not None else ''
	  
	source = entry.find("feature[@name='source']")
	[meta['Taxon ID'], meta['Taxonomy'], meta['Organism'], meta['Strain']] = _source_metadata(source)
	
	reference = entry.find("reference[@type='article']")
	[meta['Reference Location'], meta['PubMed ID']] = _reference_metadata(reference)
		
	return meta

def _entry_metadata(entry):
        if entry is None:
                return ['', '', '', '', '']
        # find molecule type, topology and keywords
        mt = entry.attrib['moleculeType']
	tp = entry.attrib['topology']
	fp = entry.attrib['firstPublic']
	lu = entry.attrib['lastUpdated']
	
	keywords = entry.findall('keyword')
	kws = ''
	if keywords is not None:
	    for kw in keywords:
	            kws += "%s; " % kw.text
	kws = kws[:-2] # remove trailing "; "
	
	return [mt, tp, kws, fp, lu]

def _source_metadata(source):
        if source is None:
                return ['', '', '', '']
        taxon_id = source.find('taxon').attrib['taxId']
    	taxonomy = ''
    	for t in source.findall('taxon/lineage/taxon'):
    	        taxonomy += "%s; " % t.attrib['scientificName']
    	taxonomy = taxonomy[:-2] # remove trailing "; "
    	o = source.find("qualifier[@name='organism']/value")
    	organism = remove_html_whitespace(o.text) if o is not None else ''
    	s = source.find("qualifier[@name='strain']/value")
    	strain = remove_html_whitespace(s.text) if s is not None else ''
    	
    	return [taxon_id, taxonomy, organism, strain]
    
def _reference_metadata(ref):
        if ref is None:
                return ['', '']
        r = ref.find("referenceLocation")
    	ref_loc = remove_html_whitespace(r.text) if r is not None else ''
    	p = ref.find("xref[@db='PUBMED']")
    	pubmed_id = p.attrib['id'] if p is not None else ''

    	return [ref_loc, pubmed_id]
    		                    	
def remove_html_whitespace(html):
        return re.sub("[\\t\\n]+", "", html)
