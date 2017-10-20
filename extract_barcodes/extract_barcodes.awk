{
    if (NR % 8 == 1 && NR > 1) {
        barcode = substr(read_pair[2], 1, 16)
        printf read_pair[1]" BX:Z:"barcode"\n"
        printf substr(read_pair[2], 17)"\n"
        printf read_pair[3]"\n"
        printf substr(read_pair[4], 17)"\n"
        printf read_pair[5]" BX:Z:"barcode"\n"
        printf read_pair[6]"\n"
        printf read_pair[7]"\n"
        printf read_pair[0]"\n"
    }
    read_pair[NR % 8] = $0
}
