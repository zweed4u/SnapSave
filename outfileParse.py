with open('outfile', 'r') as inF:
    for index, line in enumerate(inF):
        myString = "/bq/blob"
        if myString in line:
            with open('outfileFIND.txt', 'w') as f:
                f.write(line)
