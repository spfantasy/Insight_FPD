# Table of Contents
1. [Introduction](README.md#introduction)
2. [Dependencies](README.md#dependencies)
3. [Class Information](README.md#class-information)
4. [Possible Improvements](README.md#possible-improvments)

# Introduction
This is my solution on the data cleaning task for [Federal Election Commission](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). The input file should be strictly formatted under [official standart](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml). The output file are structured as follows:

1. `medianvals_by_zip.txt`

> CMTE_ID|ZIP_CODE|RUNNING_MEDIAN|NUM_OF_CONTRIB|TOTAL_AMOUNT

creating a new line as long as a valid_for_zip line was read into file

2. `medianvals_by_date.txt`

> CMTE_ID|TRANSACTION_DT|RUNNING_MEDIAN|NUM_OF_CONTRIB|TOTAL_AMOUNT

creating lines after all data, sorted by **CMTE_ID** first and **TRANSACTION_DT** next

# Dependencies

The code is compiled and ran successfully under **ubuntu 16.04 LTS** with **Python 2.7.12**
only basic modules:

`time`

`sys`

`Queue`
are used

# Class Information

## structured

Since each line in the text file is well formatted, we don't need to use regular expression to get all information need. Instead I construct as struct `structured` for information storage.

During initialization, it splits string by "|" and save useful parts into variables. Cut zipcode to 5 digit if it exceeds. It's member functions is used to test if the structured data is an valid item to calculate in `medianvals_by_zip.txt` or `medianvals_by_date.txt`

## processor
`processor` is the core class for stream process, each one of `medianvals_by_zip.txt` and `medianvals_by_date.txt` hold a different instance of processor, holding different data

each processor instance maintain a database to storage the item-to-record mapping(hashmap). For `medianvals_by_zip.txt`, it storage mapping from (CMTE_ID, ZIP_CODE) to `record`. For `medianvals_by_date.txt`, it storage mapping from (CMTE_ID, TRANSACTION_DT) to `record`.

For each line, a `structured` instance is created, and database is updated if this `structured` instance is valid for this `processor` instance. It also stores the indexs of last-updated item, for the usage of generating `medianvals_by_zip.txt` at real-time.


## record
`processor` is the class to storage amount for a single item, e.g. (CMTE_ID, ZIP_CODE) or (CMTE_ID, TRANSACTION_DT). And should support insert, median, total method as fast as possible

I constructed the data structure based on a min-heap and a max-heap and two scalar (median_low, median_large), which implements, O(1) total, O(1) median, O(lgn) insert. 

we need to save the amount of numbers in the data structure(empty, odd or even) for further accessment.
median_low, median_large points to the one(odd) or two(even) numbers that contributes to median. min_heap storage all numbers greater or equal than median, max_heap storage all numbers smaller or equal than median. 

When record is empty, the first inserted number is used to update median_low, median_large.
When record is odd length, we insert it into either min-heap or max-heap according to its value, and pop one value from the same heap, use the poped one and original one as median_low and median_large after sorting.

When record is even, we sort the inserted number together with median_low and median_large, push the smallest and largest into min-heap and max-heap, the remaining one becomes median.

The insert manipulation from above is shown to be O(lgn)

The median is always (median_low + median_large)/2 with round (as mention in the description from task), which is O(1)

We update the sum at each insertion, so that aquiring sum cost O(1)

# Possible Improvements
1. There's a risk to be OOM, using trie instead of hashmap will slightly decrease the memory usage. A more throughly solution is to use database, but performance will drop severely.
2. The system may have a insufficient support on Python 3.x or unicode characters, which should be improved furthermore.
3. I failed to download testcase from FEC, so it there might be couner cases which is not considered.