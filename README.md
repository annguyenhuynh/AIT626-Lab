# AIT626-Lab
Labs of Natural Language Processing course

* What does **FreqDist** return?
    * FreqDist return a **dictionary** with:
        * ✔ Keys = words
        * ✔ Values = counts
    * d = FreqDist(words)
    * To get all words: 
        * fd.keys()
    * To get word-count pairs:
        * fd.items()

* built-in **sorted()** function

    * *sorted(iterable, key=None, reverse=False)*

    * Parameters:

        * iterable: The sequence to be sorted (list, tuple, set, string, etc.)
        * key (Optional): A function to customize the sort order. Default is None.
        * reverse (Optional): If True, sorts in descending order. Default is False.
