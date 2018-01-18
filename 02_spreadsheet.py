total = 0
with open('./spreadsheet.txt') as sheet:
    for line in sheet:
        cells = [int(i) for i in line.strip().split(sep='\t')]
        total += max(cells) - min(cells)
print('Checksum: {}'.format(total))
