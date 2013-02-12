"""
This experiment collects the most frequent query terms in the crawled URLS.
"""

import argparse
import multiprocessing
import os
import sys
import subprocess
import tempfile
import urlparse
import warc


PROCS_POOL_SIZE = 4 # > 4 threads is a bad idea
#TMP_EXPERIMENTS_DIRECTORY = tempfile.mkdtemp()
PROCESS_STDOUT_FILENAME = None

def initialize_output_files(pid):
	"""
	For each unique ID a process produces,
	we create an output file specifically for it
	"""
	PROCESS_STDOUT_FILENAME = 'SEEDS_QUERIES_MAP_' + str(pid) + '.txt'
	sys.stdout = open(PROCESS_STDOUT_FILENAME, 'w')

def handle_warc_file(warc_file_name):
	global PROCESS_STDOUT_HANDLE

	if warc_file_name.find('.warc.gz') < 0:
		return

	if PROCESS_STDOUT_FILENAME is None:
		initialize_output_files(id(multiprocessing.current_process()))

	w = warc.open(warc_file_name)

	for record in w:
		if record.header.has_key('WARC-Target-URI'):

			record_url_parsed = urlparse.urlparse(record['WARC-Target-URI'])

			host = record_url_parsed.hostname
			queries_string = record_url_parsed.query

			queries = [x.split('=')[0] for x in queries_string.split('&')] # grabs a list of keys

			for query in queries:
				print host, query # one line per host and query combination
	print warc_file_name


def parse_cmdline_args():
	parser = argparse.ArgumentParser()
	
	parser.add_argument('job_directory', help='The heritrix job files directory')
	parser.add_argument(
		'--num-procs', 
		dest='num_procs', 
		help='Number of parallel processes that should run',
		type=int
	)

	return parser.parse_args()

if __name__ == '__main__':
	parsed = parse_cmdline_args()

	final_stats_handle = open('host_query_stats.txt', 'w')
	final_no_queries_handle = open('host_query_fuck_ups.txt', 'w')
	
	if parsed.num_procs:
		PROCS_POOL_SIZE = parsed.num_procs

	jobs_handlers_pool = multiprocessing.Pool(PROCS_POOL_SIZE)

	for root, dirs, files in os.walk(parsed.job_directory):

		if not root.find('warcs') >= 0:
			continue

		jobs_handlers_pool.map(
			handle_warc_file,
			[os.path.join(root, f) for f in files]
		)

	# at the end of this job, cat all the output files and process it further

	p = subprocess.Popen(
		'cat SEEDS_QUERIES_MAP* | sort | uniq -c | python per_host_separator.py',
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		shell=True
	)
	stdout, stderr = p.communicate()

	out = stdout.splitlines()
	err = stderr.splitlines()

	for line in out:
		final_stats_handle.write(line + '\n')

	for line in err:
		final_no_queries_handle.write(line + '\n')

	# remove the intermediate files generated
	os.system('rm SEEDS_QUERIES_MAP_*')