#!/usr/bin/awk -f
BEGIN{
    attach_in_readname = 1;
    attach_in_comment = 1;
    
    for (i = 1; i < ARGC; i++) {
        if (ARGV[i] == "-n")
            attach_in_readname = 0
        else if (ARGV[i] == "-c")
            attach_in_comment = 0
        else if (ARGV[i] ~ /^-./) {
            e = sprintf("%s: unrecognized option -- %c",
                    ARGV[0], substr(ARGV[i], 2, 1))
            print e > "/dev/stderr"
        } else
            break
        delete ARGV[i]
    }
    
}
{
    if (NR % 8 == 1 && NR > 1) {
        read_name1 = substr(read_pair[1], 1, match(read_pair[1], / /) - 1)
        read_name2 = substr(read_pair[5], 1, match(read_pair[5], / /) - 1)
        
        if (read_name1 != read_name2){
            print "Read pairs at line " NR " do not interleave correctly: " read_pair[1] "\t" read_pair[5] ;
        } else {
            barcode = substr(read_pair[2], 1, 16);
            
            if (attach_in_readname) {
                initial = "@"barcode"-1_";
                read_pair[1] = substr(read_pair[1], 2)
                read_pair[5] = substr(read_pair[5], 2)
            }           
            
            if (attach_in_comment) {
                final = " BX:Z:"barcode"-1";
            }
            
            printf initial read_pair[1] final"\n"
            printf substr(read_pair[2], 17)"\n"
            printf read_pair[3]"\n"
            printf substr(read_pair[4], 17)"\n"
            printf initial read_pair[5] final"\n"
            printf read_pair[6]"\n"
            printf read_pair[7]"\n"
            printf read_pair[0]"\n"        
        }
    }
    read_pair[NR % 8] = $0
}
