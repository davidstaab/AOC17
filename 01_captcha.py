
# [dstaab] server is rejecting my requests. not worth figuring out which headers need to be included.
#
# import requests as req
#
# cmn_headers = {
#     'User-Agent': 'Python-urllib/3.1'
# }
#
# resp = req.get('https://adventofcode.com/2017/day/1/input', headers=cmn_headers)
# resp.raise_for_status()  # no-op on OK

next_sum = 0
halfway_sum = 0
with open('./captcha.txt') as stream:
    seq = stream.read().strip()
    halfway = int(len(seq) / 2)  # int cast guaranteed safe by exercise instructions
    for this_dig, next_dig, half_dig in zip(seq, seq[1:] + seq[0], seq[halfway:] + seq[0:halfway]):
        if this_dig == next_dig:
            next_sum += int(this_dig)
        if this_dig == half_dig:
            halfway_sum += int(this_dig)
print('Next-element Sum: {}'.format(next_sum))
print('Halfway-around Sum: {}'.format(halfway_sum))
