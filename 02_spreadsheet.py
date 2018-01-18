checksum = 0
divis_sum = 0

with open('./spreadsheet.txt') as sheet:
    for line in sheet:
        cells = [int(i) for i in line.strip().split(sep='\t')]

        # PART 1
        checksum += max(cells) - min(cells)

        # PART 2
        cells.sort(reverse=True)  # Sort desc to speed up divisibility search, since a / b < 1 is invalid
        for i in range(len(cells)):
            for other in cells[i+1:]:
                rem = cells[i] % other
                if rem == 0:
                    divis_sum += int(cells[i] / other)
                    break  # End search within line once found

print('Checksum: {}'.format(checksum))
print('Evenly Divisible Pairs Sum: {}'.format(divis_sum))
