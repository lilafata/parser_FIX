
##########################################################################################################
#
# DATE  :      05/23/2018
# AUTHOR:      Lila Fata
# FILE  :      parser_FIX.py
# DESCRIPTION: This script file contains the following five functions to download a 'secdef' zipped file
#              from the CME Group public FTP site, unzipped the secdef file, parses the file, extract
#              certain data from the file to answer the three questions below, and prints the results to
#              the output screen.
#
#              * download_secdef_zipfile() - download and unzip secdef.dat.gz file from FTP cmegroup
#              * parse_secdef_file() - parse and extract relevant data and store in dictionaries
#              * print_solution1() - prints output of solution to question 1
#              * print_solution2() - prints output of solution to question 2
#              * print_solution3() - prints output of solution to question 3
#
#              Q1) How many instruments of each security type (tag 167) exist?
#              Q2) How many futures (tag 167) instruments exist in each product complex (tag 462)?
#              Q3) What are the names (tag 55) of the earliest four expirations (tag 200) for the
#                  futures (tag 167) instruments with asset (tag 6937) 'GE' and have zero legs (tag 555)?
#
# ASSUMPTIONS: Following assumptions are based on analyzing the secdata.DAT file provided in the
#              'Python Exercise 05.17.2018' zipped attachment:
#
# 1) Each column is delimited by the Start of Header (SOH)
# 2) There are up to five possible security types: 'FUT', 'OOF', 'MLEG', 'IRS', 'FXSPOT'
# 3) There are up to eight possible product complex: '2', '4', '5', '12', '14', '15', '16', '17'
# 4) Names/Symbols (tag 55) are unique
# 5) The tags (ie. 6937, 55, 167, 200, 555) are not necessarily on same column in each secdef.DAT file,
#    so parser goes through each column until it finds the correct tag field.  Therefore, this takes
#    longer as opposed to directly indexing into the column field to get the tag data.
#
# NOTE:
# 1) This program was executed using the IDLE Python 3.7 Shell on a Windows 10 laptop
#
##########################################################################################################

import os
import urllib.request
import gzip
import shutil

SOH = '\x01'                        # Delimiter Start Of Header (SOH) in secdef.DAT file
SECURITY_TYPE_TAG = '167'           # Security Type (tag 167)
FUTURES = 'FUT'                     # Futures (tag 167) Instrument
UNDERLYING_PRODUCT_TAG = '462'      # Product Complex (tag 462)
ASSET_GE = '6937=GE'                # Asset=GE (tag 6937)
NOLEGS_TAG = '555'                  # NoLegs (tag 555)
NAMES_TAG = '55'                    # Name / Symbol (tag 55)
EXPIRATION_TAG = '200'              # Expiration / MaturityMonthYear (tag 200)

# Dictionary to store number of instruments (initialized to 0) for each security type
d167 = {}
d167.setdefault('FUT', 0)
d167.setdefault('OOF', 0)
d167.setdefault('MLEG', 0)
d167.setdefault('IRS', 0)
d167.setdefault('FXSPOT', 0)

# Dictionary to store number of futures instruments (initialized to 0) for each product complex
d462 = {}
d462.setdefault('2', 0)
d462.setdefault('4', 0)
d462.setdefault('5', 0)
d462.setdefault('12', 0)
d462.setdefault('14', 0)
d462.setdefault('15', 0)
d462.setdefault('16', 0)
d462.setdefault('17', 0)

# Dictionary to store names / expirations for futures instruments with asset 'GE' and zero legs
dNameExpiration = {}

##########################################################################################################
# FUNCTION:    download_secdef_zipfile()
# DESCRIPTION: Downloads secdef.dat.gz zipped file from ftp.cmegroup.com, and unzips file, and stores
#              in current working directory
# INPUT:       secdef.dat.gz zipped file from FTP cmegroup.com
# OUTPUT:      secdef.DAT file
##########################################################################################################
def download_secdef_zipfile():
    print("\nDownloading 'secdef.dat.gz' zip file from ftp.cmegroup.com...\n")
    current_dir = os.getcwd()
    print ("Working directory is ", current_dir)
    try:
        url = 'ftp://ftp.cmegroup.com/SBEFix/Production/secdef.dat.gz'  #URL of CME Group public FTP site
        secdefzip_filename = 'secdef.dat.gz'
        urllib.request.urlretrieve(url, secdefzip_filename)  #Get zipped secdef file from the FTP site

        print("\nDownload complete...\n")
        zipfilepath = os.path.realpath(secdefzip_filename)
        print ("Path of zipped file is ", zipfilepath)

        print("\nUnzipping 'secdef.dat.gz' file...\n")
        with gzip.open(zipfilepath, 'rb') as sfile_in:     #Unzip and store secdef file in current directory
            with open('secdef.DAT', 'wb') as sfile_out:
                shutil.copyfileobj(sfile_in, sfile_out)
        secdef_filename = 'secdef.DAT'            
        filepath = os.path.realpath(secdef_filename)
        print ("Path of unzipped file is ", filepath)
        return True
    except:
        print("\nDownload FTP error!\n")
        return False                                 

##########################################################################################################
# FUNCTION:    parse_secdef_file()
# DESCRIPTION: Parses secdef.DAT file, extracts and stores relevant data in dictionaries for solutions
#              to the three questions
# INPUT:       secdef.DAT file
# OUTPUT:      Dictionaries with extracted data from secdef.DAT file
##########################################################################################################
def parse_secdef_file():
    print("\nParsing secdef.DAT file...\n")
    secdef_filename = 'secdef.DAT'            
    secdef_filepath = os.path.realpath(secdef_filename)
    try:
        with open(secdef_filepath, 'r') as secdefFile:  #Open secdef.DAT file for read
            for line in secdefFile:        #For each row in the file
                field = line.split(SOH)    #Get all fields/columns separated by SOH delimiter
                futures = False
                assetGE = False
                nolegs = False
                underlying_product = False
                for data in field:         #For each data in field/column
                    if (data.split('=')[0] == SECURITY_TYPE_TAG):  #If security type tag 167
                        d167[data.split('=')[1]] += 1              #Store number of instruments for this security type
                        if (data.split('=')[1] == FUTURES):        #If futures instrument
                            futures = True
                    elif (data.split('=')[0] == UNDERLYING_PRODUCT_TAG): #If tag 462, increment number for this product complex
                        underlying_product = True
                        product_complex = data.split('=')[1]      #Get product complex                
                    elif (data == ASSET_GE and not assetGE):      #If asset GE (6937=GE)
                        assetGE = True
                    elif (data.split('=')[0] == NOLEGS_TAG):      #If nolegs data (tag 555)
                        nolegs = True
                    elif (data.split('=')[0] == NAMES_TAG):       #If names data (tag 55)
                        names = data.split('=')[1]
                    elif (data.split('=')[0] == EXPIRATION_TAG):  #If maturity month/year expiration data (tag 200)
                        expiration = data.split('=')[1]
                if futures:                                   #Futures instrument
                    if underlying_product:                    #Underlying product (tag 462)
                        #d462.get(product_complex, 0)
                        d462[product_complex] += 1            #Store number of futures instruments for this product complex
                    if assetGE and not nolegs:                #Asset = 'GE' with zero legs
                        dNameExpiration[names] = expiration   #Store names and expiration
        return True
    except FileNotFoundError:
        print("\nFile not found error!\n")
        return False                         
    except KeyError:
        print("\nFile parse/process error!\n")
        return False                 

##########################################################################################################
# FUNCTION:    print_solution1()
# DESCRIPTION: Prints output of solution to Question 1: How many instruments of each security type
#              (tag 167) exist?
# INPUT:       Dictionary d167{}
# OUPPUT:      Data output to screen containing answer to question 1
##########################################################################################################
def print_solution1():
    print("\nHere's the output of solution to question 1...\n")
    for key,val in d167.items():
        print(key, " has ", val, "instruments")

##########################################################################################################
# FUNCTION:    print_solution2()
# DESCRIPTION: Prints output of solution to Question 2: How many futures (tag 167) instruments exist
#              in each product complex (tag 462)?
# INPUT:       Dictionary d462{}
# OUTPUT:      Data output to screen containing answer to question 2
##########################################################################################################
def print_solution2():
    print("\nHere's the output of solution to question 2...\n")
    for key,val in d462.items():
        print("Product complex ", key, " has ", val, "futures instruments")

##########################################################################################################
# FUNCTION:    print_solution3()
# DESCRIPTION: Prints output of solution to Question 3: What are the names (tag 55) of the earliest
#              four expirations (tag 200) for the futures (tag 167) instruments with asset (tag 6937)
#              'GE' and have zero legs (tag 555)?
# INPUT:       Dictionary dNameExpiration{}
# OUTPUT:      Data output to screen containing answer to question 3
##########################################################################################################
def print_solution3():
    sortedExpirationName = sorted(dNameExpiration.items(), key=lambda x: x[1]) #Sort by expiration date
    print("\nHere's the output of solution to question 3...\n")
    for key,val in sortedExpirationName[:4]:                        #Get first four earliest expirations
        print ("Name: ", key, " has expiration: ", val)

##########################################################################################################
# FUNCTION:    main()
# DESCRIPTION: Performs the following tasks:
#              1) Download the secdef.dat.gz file from FTP cmegroup
#              2) Parses secdef.DAT file and extracts data for solutions to the three questions
#              3) Prints output of solution to question 1
#              4) Prints output of solution to question 2
#              5) Prints output of solution to question 3
# INPUT:       CME Group FTP site with a secdef.dat.gz file
# OUTPUT:      Data output to screen containing answers to three questions
##########################################################################################################
def main():
    if (download_secdef_zipfile()):  #Download and unzip secdef.dat.gz file from CME Group public FTP site
        if (parse_secdef_file()):    #Parse and extract data from secdef.DAT file
            print_solution1()        #Output solution for solution 1 to screen
            print_solution2()        #Output solution for question 2 to screen
            print_solution3()        #Output solution for question 3 to screen
        else:
            print("\nError in parse_secdef_file()...exiting program\n")
    else:
        print("\nError in download_secdef_zipfile()...exiting program\n")

if __name__ == "__main__":
    main()
