


import oeis, sys, time



def print_log(*args, **kwargs):
	print(*args, **kwargs)
	print(*args, **kwargs, file=sys.stderr)



oeis.load_data()

if len(sys.argv)>1:
	subseq = list(map(int,sys.argv[1:]))
else:
	print('no subsequence provided')
	exit(1)



print(f'searching for contiguous subsequence \'{subseq}\' ')
time.sleep(1)

for num in oeis.existing_entry_numbers():
	S = oeis.OEISSequence(num)
	if S.has_subsequence(subseq):
		print_log(f'OEIS #{num}: {S.description}')
		time.sleep(0.1)



