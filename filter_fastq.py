#!/usr/bin/python

# Filename:    filter_fastq.py
# Version:     2014-10-20
# Description: Program to remove invalid data records from fastq files.
# References:  http://en.wikipedia.org/wiki/FASTQ_format
#              http://www.bioperl.org/wiki/Fastq
#              http://maq.sourceforge.net/fastq.shtml
# Author:      Brian High <high@uw.edu>
# License:     GNU General Public License version 3 (GPLv3) or higher.
#              See: http://www.gnu.org/licenses/gpl.html
# Usage:       python filter_fastq.py input_file > output_file
#
# A fastq record is valid only if it satisfies these requirements:
#
#  1. The record is exactly 4 lines of text (id1, seq, id2, qual).
#  2. The first "sequence name" line (id1) starts with @ ("at" sign).
#  3. The third "sequence name" line (id2) starts with + ("plus" sign).
#  4. Sequence (seq) and quality (qual) lines must have same length.
#
# NOTE:
#
#     Since the fourth line might start with @, we will
#     actually use @SRR as our record separator to reduce
#     the chances of mistaking a fourth line for a new record.
#     Change this (rec_sep) to match your data ID string.

import sys, os

# ----------------------------
# Initialize Global Variables
# ----------------------------

rec_sep = '@SRR'
filename = ''
lines_per_record = 4

# ----------
# Functions
# ----------

# Iterate a through a file with a user-definable record separator.
# Since Python doesn't have something like Perl's 
# $INPUT_RECORD_SEPARATOR ($/), we need a custom 
# function. Fortunately, one has been written for us:
# http://bugs.python.org/issue1152248 - msg109117 - Douglas Alan
def fileLineIter(inputFile,
                 inputNewline="\n",
                 outputNewline=None,
                 readSize=8192):
   """Like the normal file iter but you can set what string indicates newline.
   
   The newline string can be arbitrarily long; it need not be restricted to a
   single character. You can also set the read size and control whether or not
   the newline string is left on the end of the iterated lines.  Setting
   newline to '\0' is particularly good for use with an input file created with
   something like "os.popen('find -print0')".
   """
   if outputNewline is None: outputNewline = inputNewline
   partialLine = ''
   while True:
       charsJustRead = inputFile.read(readSize)
       if not charsJustRead: break
       partialLine += charsJustRead
       lines = partialLine.split(inputNewline)
       partialLine = lines.pop()
       for line in lines: yield line + outputNewline
   if partialLine: yield partialLine

# -------------
# Main Routine
# -------------

# Read filename argument from command line
if len(sys.argv) > 1: filename = sys.argv[1]
if filename == '':
    print "Usage: python filter_fastq.py FILENAME"
    sys.exit(1)

# Make sure the file exists
if not os.path.exists(filename):
    print "Filename " + filename + " cannot be found."
    sys.exit(1)

# Process fastq data by multi-line record.
for record in fileLineIter(open(filename, 'rb'), rec_sep):
    
    # Split record into lines.
    lines = record.splitlines()
    
    # Skip records with less than lines_per_record lines.
    if len(lines) < lines_per_record: continue
    
    # Assign a variable to each line. Ignore extra lines.
    (id1, seq, id2, qual) = lines[:lines_per_record]
    
    # Prepend the record separator to first line (if missing).
    if not id1.startswith(rec_sep): id1 = rec_sep + id1
    
    # Skip records where sequence and quality lines are not same length.
    if len(seq) != len(qual): continue
    
    # Skip records where 3rd line (2nd ID line) doesn't start with '+'.
    if not id2.startswith('+'): continue
    
    # Print the 4 required lines to make a valid record.
    print "\n".join((id1, seq, id2, qual))
