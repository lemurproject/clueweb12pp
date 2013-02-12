"""
On STDIN we are supplied a list of type:
Freq, hostname, query.

We isolate the top items on this list.
"""

import sys


HOSTNAME_TOP_QUERIES_MAP = {}

def handle_host_query_freq_tuples(freq, hostname, query):
	global HOSTNAME_TOP_QUERIES_MAP

	if not HOSTNAME_TOP_QUERIES_MAP.has_key(hostname):
		HOSTNAME_TOP_QUERIES_MAP[hostname] = [(query, freq)]

	elif len(HOSTNAME_TOP_QUERIES_MAP[hostname]) < 3:
		HOSTNAME_TOP_QUERIES_MAP[hostname].append((query, freq))

	else:
		contenders = [(query, freq)].extend([q_qfreq for q_qfreq in HOSTNAME_TOP_QUERIES_MAP[hostname]])
		contenders.sort(key = lambda x : x[1])
		HOSTNAME_TOP_QUERIES_MAP[hostname] = contenders[0:3]

if __name__ == '__main__':

	for line in sys.stdin:

		try:
			freq, hostname, query = line.split()
			handle_host_query_freq_tuples(int(freq), hostname, query)

		except:
			sys.stderr.write(hostname + '\n')

	for host in HOSTNAME_TOP_QUERIES_MAP.keys():
		for query in HOSTNAME_TOP_QUERIES_MAP[host]:
			print host, query[0], query[1]
		print # for extra newline to separate hostnames