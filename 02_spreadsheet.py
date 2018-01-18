checksum = 0
divis_sum = 0


def divide(divisor: float, dividends: list) -> int:
    """
    Divides a value by each other value in a list. When a clean division is found, returns the quotient. If no clean
    division is found, returns 0.

    :return: Quotient, if a clean division is found, or 0
    """
    for dividend in dividends:
        rem = divisor % dividend
        if rem == 0:
            return int(divisor / dividend)
    return 0


with open('./spreadsheet.txt') as sheet:
    for line in sheet:
        cells = [int(i) for i in line.strip().split(sep='\t')]

        # PART 1
        checksum += max(cells) - min(cells)

        # PART 2
        cells.sort(reverse=True)  # Sort desc to speed up divisibility search, since a / b < 1 is invalid
        for i in range(len(cells)):
            val = divide(cells[i], cells[i + 1:])
            divis_sum += val
            if val != 0:
                break

print('Checksum: {}'.format(checksum))
print('Evenly Divisible Pairs Sum: {}'.format(divis_sum))
