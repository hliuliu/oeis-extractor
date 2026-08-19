

import oeis, sys, time

oeis.load_data()



for i,num in enumerate(oeis.existing_entry_numbers()):
	S = oeis.OEISSequence(num)
	desc = S.description
	S.remove_description()
	if desc!=S.description:
		print(f'OEIS #{num}: {desc}')
		print(f'\tOEIS #{num}: {desc}', file=sys.stderr)
		S.description=desc
		# time.sleep(0.3)
	print(f'processed {i+1} of {oeis.num_available_sequences()}', file=sys.stderr)
