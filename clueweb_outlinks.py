"""
Gathers a list of outlinks from Clueweb12
"""

#!/usr/bin/env python

import chardet
import os
import sys
import warc

from BeautifulSoup import BeautifulSoup, SoupStrainer


def handle_warc_file(warc_file):
	f = warc.open(warc_file)

	for warc_record in f:
		handle_warc_record(warc_record)

def handle_warc_record(record):
	s = record.payload.read()

	for link in BeautifulSoup(s, SoupStrainer('a')):
		if link.has_key('href'):
			s = link['href']

			try:
				print s

			except UnicodeEncodeError:
				continue # should have used chardet but it failed with a weak check.

		sys.stdout.flush()
	

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print "Usage: python clueweb_outlinks.py <diskno.>"
		sys.exit(1)

	clueweb_disk = sys.argv[1]
	clueweb_output_file = sys.argv[2]
	sys.stdout = open(clueweb_output_file, 'w')
	for root, dirs, files in os.walk(clueweb_disk):
		warc_files = filter(
			lambda s: s.find('warc.gz') >= 0,
			files
		)

		for warc_file in warc_files:
			warc_file_path = os.path.join(root, warc_file)

			handle_warc_file(warc_file_path)