# parser_FIX
This python script downloads the zipped secdef.dat file from CME public FTP site, parses it and extracts specific data from that file.
The secdef.dat file is a huge file and contains rows/columns of data from the FIX (Financial Exchange Information) protocol.
The sample file 'secdef.data.gz' included in this gitbhub has ~25000 rows.

The goal is to write a parser without using libraries from Python such as:  pandas module or similar data-processing modules.

