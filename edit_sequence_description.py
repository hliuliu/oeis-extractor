

import oeis, sys


oeis.load_data()

if len(sys.argv)>1:
	S = oeis.OEISSequence(int(sys.argv[1]))
else:
	S = oeis.random_available_sequence()

print(S)

print('select an option for this sequence.') 

for i, msg in enumerate([
		'add/edit description',
		'remove description'
	],1):
	print(f'{i}. {msg}')


opt = int(input())
if opt not in [1,2]:
	raise ValueError(f'Invalid option: {opt}')


if opt==1:
	print(f'current or suggested description:\n{S.description}')
	opt = input('Apply this suggestion? (Y/N) ')
	if opt.upper().strip()=='N':
		desc = input('Enter a custom description.\n')
		if not desc.strip():
			print('No description entered.')
			exit(1)
		print(f'You are about to set the description:\n{desc}')
		S.description = desc
elif opt==2:
	S.remove_description()

opt = input('save changes? (Y/N) ')
if opt.upper().strip()=='Y':
	S.commit_data()
	oeis.save_data()
	print('changes saved.')
