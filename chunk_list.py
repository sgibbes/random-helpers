import pprint


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
        
 
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

chunk_list = list(chunks(l, 3))

for i in chunk_list:
    print i
    