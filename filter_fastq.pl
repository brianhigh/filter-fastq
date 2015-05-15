#!/usr/bin/perl

# Filename:    filter_fastq.pl
# Version:     2014-03-08
# Description: Program to remove invalid data records from fastq files.
# References:  http://en.wikipedia.org/wiki/FASTQ_format
#              http://www.bioperl.org/wiki/Fastq
#              http://maq.sourceforge.net/fastq.shtml
# Author:      Brian High <high@uw.edu>
# License:     GNU General Public License version 3 (GPLv3) or higher.
#              See: http://www.gnu.org/licenses/gpl.html
# Usage:       perl filter_fastq.pl < input_file > output_file
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
#     Change this ($rec_sep) to match your data ID string.

use English '-no_match_vars';
use warnings;
use strict;

# For $rec_sep, we would use just '@', but '@' can begin 4th line.
# Edit $rec_sep as needed to match your ID string (the common part).
my $rec_sep = '@SRR';
local $INPUT_RECORD_SEPARATOR = "\n$rec_sep";

# Process fastq data by multi-line block (i.e. "record").
while (<>) {

    # Split block into lines where "\n" is the end-of-line.
    my @lines = split /\n/, $_;

    # Skip blocks with less than 4 lines.
    next unless $#lines >= 3;

    # Assign a variable to each line. Ignore any excess lines.
    my ($id1, $seq, $id2, $qual) = @lines;

    # Prepend the record separator to first line (if missing).
    $id1 = $rec_sep . $id1 unless $id1 =~ m/^$rec_sep/;

    # Skip blocks where sequence and quality lines are not same length.
    next unless length( $seq ) == length( $qual );

    # Skip blocks where 3rd line (2nd ID line) doesn't start with '+'.
    next unless $id2 =~ m/^[+]/;

    # Print the 4 required lines of the block to make a valid record.
    print "$id1\n$seq\n$id2\n$qual\n";
}
