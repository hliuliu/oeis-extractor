

import oeis, sys, time

oeis.load_data()

if len(sys.argv)>1:
	desc = sys.argv[1]
else:
	print('no description argument provided')
	exit(1)


desc = desc.lower()

print(f'searching with keyword \'{desc}\' ')
time.sleep(1)

for num in oeis.existing_entry_numbers():
	S = oeis.OEISSequence(num)
	if desc in S.description.lower():
		print(f'OEIS #{num}: {S.description}')
		time.sleep(0.3)




