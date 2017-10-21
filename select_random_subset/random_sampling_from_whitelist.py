import random
from operator import itemgetter

out_file = open("subset", "w+")
in_file  = open("barcode")
sample = set(random.sample(range(0, 4000000), 4500))
sample = list(sample)[0:4000]
for line in itemgetter(*sample)(in_file.readlines()):
    print(line.rstrip(), file=out_file)
