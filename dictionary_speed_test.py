import time

from crossword.dictionary import Dictionary

dictionary = Dictionary()
start = time.time()
query = "A   "
count = 500
for i in range(0, count):
    dictionary.search(query)
    dictionary.search.cache_clear()

seconds = time.time() - start
print(f"{count / seconds:.2f} searches/sec")
