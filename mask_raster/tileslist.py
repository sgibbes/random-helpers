import subprocess
cmd = ['aws', 's3', 'ls', 's3://gfw-files/sam/carbon_budget/carbon_030218/litter/', '>', 'tiles.txt']
subprocess.check_call(' '.join(cmd), shell=True)

tl = []
with open('tiles.txt', 'r') as thefile:
    for l in thefile:
        tl.append(l.split(' ')[-1].replace('_litter.tif', '').strip('\n'))

print tl
