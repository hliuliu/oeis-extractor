

import oeis


oeis.load_data()

for num in oeis.existing_entry_numbers():
	print(f'reloading OEIS #{num}')
	oeis.OEISSequence(num).reload_sequence()
	oeis.OEISSequence(num).commit_data()

oeis.save_data()





