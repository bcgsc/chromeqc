# Usage
```
python3 random_sampling_from_whitelist [arguments and their values]
```
# Arguments
```
-w --whitelist     : default='whitelist_barcodes', type=str
-k --subsample_size: default=4000                , type=int
-i --in            : default='-'                 , type=str
-o --out           : default='stdout'            , type=str
-s --seed          : default=1334                , type=int
-m --max_read_pairs: default=-1                  , type=int, note: -1 means all read pairs
-p --stats_out_path: default='.'                 , type=str, note: the directory needs to be created already
-v --verbose       : default=True                , type=bool, note: True or False values only   
```
