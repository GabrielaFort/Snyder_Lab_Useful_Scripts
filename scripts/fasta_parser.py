# This function takes an input fasta file and parses it into a list of sequences
# from the file, even if the sequences fall on different lines
def parse_fasta(input_file):
    with open(input_file, 'r') as fasta:
        seq_list = []
        seq_string = ''
        for line in fasta:
            line=line.rstrip()
            if line.startswith('>'):
                if seq_string:
                    seq_list.append(seq_string)
                seq_string = ''
            else:
                seq_string += line

        seq_list.append(seq_string)

    return seq_list


                

