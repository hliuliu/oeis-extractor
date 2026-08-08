

import sys, oeis


oeis.load_data()

if len(sys.argv)>1:
	S = oeis.OEISSequence(int(sys.argv[1]))
else:
	S = oeis.random_available_sequence()

print(S)






