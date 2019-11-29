#!/usr/bin/env python3
# Author: Sylvain Carlioz
# 6/03/2017
# Updated : Manoj Moktan
# 2019/11/20

# MIT license -- free to use as you want, cheers.

"""
Simple python wrapper script to use ghoscript function to compress PDF files.

Compression levels:
    0: default
    1: prepress
    2: printer
    3: ebook
    4: screen

Dependency: Ghostscript.
On MacOSX install via command line `brew install ghostscript`.
"""

import argparse
import subprocess
import os.path
import sys
from shutil import copyfile
import argparse
from pathlib import Path
# Folder wise path
# python pdf_compressor.py "E:\python-project\pdfc\filebox\src" -o "E:\python-project\pdfc\filebox\compress" -c 2 -cm 1
#  File wise path
# python pdf_compressor.py "E:\python-project\pdfc\filebox\src\test.pdf" -o "E:\python-project\pdfc\filebox\compress" -c 2 -cm 0
#define  global variable for root  source  from given argument
__srcFolder = ''
def compress(input_file_path, output_file_path,  power=0):
    """Function to compress PDF via Ghostscript command line interface"""
    # follow below  link for  configure  pdf file
    # http://milan.kupcevic.net/ghostscript-ps-pdf/
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }
    
    # -dPDFSETTINGS=/default  (almost identical to /screen)
    # -dPDFSETTINGS=/prepress (high quality, color preserving, 300 dpi imgs)
    # -dPDFSETTINGS=/printer  (high quality, 300 dpi images)
    # -dPDFSETTINGS=/ebook    (low quality, 150 dpi images)
    # -dPDFSETTINGS=/screen   (screen-view-only quality, 72 dpi images)

    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file")
        sys.exit(1)

    # Check if file is a PDF by extension
    # if input_file_path.split('.')[-1].lower() != 'pdf':
    #     print("Error: input file is not a PDF")
    #     sys.exit(1)
    print("===================================================================")
    print("Compressing PDF...")
    print("Input File Name :", input_file_path)
    print("OutPut File Name :",output_file_path)
    # print(sys.version)
    initial_size = os.path.getsize(input_file_path)
    # print(os.path)

    # do define gswin64c for hide ghostwin window while  compressing file
    # do define gswin64  if you  want to show ghostwin window while  compressing file 
    # filename can get  from path C:\Program Files\gs\gs9.50\bin
    subprocess.call(['gswin64', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS={}'.format(quality[power]),
                    '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(output_file_path),
                     input_file_path]
    )
    final_size = os.path.getsize(output_file_path)
    print("initial Size Of File::",initial_size)
    print("Final size of File ::",final_size)
    
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.1f}MB".format(final_size / 1000000))
    print("Done.")


def getListOfFiles(dirName,outputDirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # split source folder  for  create sub directory
        splitSrcFolderName = dirName.split(__srcFolder)
        if len(splitSrcFolderName) > 0:
            # If filename directory is not exist  then  create  directory
            outputFullPath = outputDirName + splitSrcFolderName[1]
            if not os.path.exists(outputFullPath):
                os.makedirs(outputFullPath)
               
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath,outputDirName)
        else:
            allFiles.append(fullPath)

    return allFiles        


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', help='Relative or absolute path of the input PDF file')
    parser.add_argument('-o', '--out', help='Relative or absolute path of the output PDF file')
    parser.add_argument('-c', '--compress', type=int, help='Compression level from 0 to 4')
    parser.add_argument('-cm', '--cm', default=0,type=int, help='Compress method  single  File or  Folder  Wise')
    parser.add_argument('-b', '--backup', action='store_true', help="Backup the old PDF file")
    parser.add_argument('--open', action='store_true', default=False,
                        help='Open PDF after compression')
    
    args = parser.parse_args()
    globals()['__srcFolder'] = args.input 
    # In case no compression level is specified, default is 2 '/ printer'
    if not args.compress:
        args.compress = 2
    # In case no output file is specified, store in temp file
    if not args.out:
        args.out = 'temp.pdf'
    # In case compress method  equals to 0 than check  file  exist or not  and  compress method equals to 1 than check folder exist or not:
    if args.cm == 0:
        if not os.path.isfile(args.input):
           print('Input File Does Not  Exist !')
           sys.exit(1)
    else:
        if not os.path.isdir(args.input):
            print('Input Folder Does Not  Exist !')
            sys.exit(1)

    inputFile = ''
    outPutFile = ''

    # list the file  of given argument directory is specific filename exist
    # filename = os.listdir(args.input)
    # compress file name  through absolute  path when compress method is 0
    if args.cm == 0:
        inputFilePathName = os.path.basename(args.input)
        if inputFilePathName.split('.')[-1].lower()!='pdf':
            print("Error: input file is not a PDF")
            sys.exit(1)

        filename = os.path.basename(args.out)
        filename =  filename.lower()
        outPutFile = filename.split('.pdf')
        if len(outPutFile) > 1:
            outPutFile = args.out
        else:
            outPutFile = args.out + '/' + inputFilePathName
        
        compress(args.input, outPutFile, power=args.compress)
    else:
         # compress file name  through folder wise when compress method is 1
         # list all  root directory , directory/sub-directory, file in filename  variable
        filename = [os.path.join(r, file) for r, d, f in os.walk(args.input) for file in f]
        # create directory, sub-directory if not exist from  getListOfFiles function
        listOfFiles = getListOfFiles(args.input, args.out)
        for file in filename:
            splitFolderName = file.split(args.input)
            outPutFile = args.out  + splitFolderName[1]
            inputFile = file
            if inputFile.split('.')[-1].lower()!='pdf':
                continue

            compress(inputFile, outPutFile, power=args.compress)
        
    # In case no output file is specified, erase original file
    if args.out == 'temp.pdf':
        if args.backup:
            copyfile(args.input, args.input.replace(".pdf", "_BACKUP.pdf"))
        copyfile(args.out, args.input)
        os.remove(args.out)

    # In case we want to open the file after compression
    if args.open:
        if args.out == 'temp.pdf' and args.backup:
            subprocess.call(['open', args.input])
        else:
            subprocess.call(['open', args.out])



if __name__ == '__main__':
    main()
