"""
Gathers a list of outlinks from Clueweb12
"""

#!/usr/bin/env python

import os
import sys
import warc


CLUEWEB_DATASET_PATH = '/Users/shriphani/Documents'
CLUEWEB_DISK = None

CLUEWEB_DISK_DATA_DIRS_PATTERN = r'ClueWeb12_[0-9][0-9]' #each clueweb disk hands data off in this fashion
CLUEWEB_DISK_WEB_CRAWLS_PATTERN = r'[0-9][0-9][0-9][0-9]wb' #web crawls contain wb

def main():
	"""
	Runs the disk job
	"""
	

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print "Usage: python clueweb_outlinks.py <diskno.>"
		sys.exit(1)

	CLUEWEB_DISK = sys.argv[1]
	for root, dirs, files in os.walk(os.path.join(CLUEWEB_DATASET_PATH, CLUEWEB_DISK)):
		print root, dirs, files