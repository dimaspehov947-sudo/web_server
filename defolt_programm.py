from Bio.Data import IUPACData


def is_dna(sequence):
    sequence = sequence.strip().upper()

    if len(sequence) > 20:
        return "Последовательность превышает допустимый лимит символов"
    
    if not sequence:
        return "Путая строка"

    good_simbols = set(IUPACData.ambiguous_dna_letters)
    for i in sequence:
        if i not in good_simbols:
            return "Последовательность содержит недопустимые символы"
        
    return 'Последовательность прошла проверку'


print(is_dna("GATCRYWSMkhBVDN"))
