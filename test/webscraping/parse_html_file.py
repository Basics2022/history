"""

"""

import re

filen = 'output.html'
substring = '"title":{"runs":[{"text"'   # string before the title of the videos
substring = re.escape(substring)
len_sub = 24 # len(substring)
print(len(substring))

check_str = 100

with open(filen, 'r') as f:
    s = f.read()

matches = re.finditer(substring, s)
print(matches)
n_match = 0
for match in matches:
    # print(f"match at position {match.start()}")
    ini = match.start() + len_sub
    print(s[match.start():match.start()+check_str])
    print(n_match ,': ', s[ini:ini+check_str])
    n_match += 1
