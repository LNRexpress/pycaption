#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import argparse
import codecs
import sys
#sys.path.append("/Users/ckane/sandbox/pycaption-fork")
sys.path.append("..")
#from pycaption import (DFXPReader, SAMIWriter, SCCWriter, SRTWriter, DFXPWriter, TranscriptWriter, WebVTTWriter, detect_format)
from pycaption import (DFXPReader, SAMIWriter, SCCReader, SCCWriter, SRTWriter, DFXPWriter, WebVTTWriter, detect_format)


def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='Caption file converter.')
    parser.add_argument('-i','--input', help='Input file name',required=True)
    parser.add_argument('-o','--output',help='Output file name', required=True)
    parser.add_argument('-f','--format',help='Output caption format (dfxp, sami, scc, srt, transcript, or vtt)', required=True)
    args = parser.parse_args()

    # Get the parsed arguments
    input_file_path = args.input
    output_file_path = args.output
    output_format = args.format

    # Open and read the source file
    f = codecs.open(input_file_path, 'r', 'utf-8')
    text = f.read()
    f.close()

    # Detect the input caption format, create the appropriate reader, and
    # convert the contents of the caption file into an intermediate representation
    reader = detect_format(text)
    reader = reader()

    # Force the DFXPReader to read positioning information from the caption elements
    if type(reader) is DFXPReader:
        reader.read_invalid_positioning = True

    captions = reader.read(text)

    # Finally, write the intermediate representation of the captions to the output file
    f = codecs.open(output_file_path, 'w', 'utf-8')

    if output_format == 'dfxp':
        f.write(DFXPWriter().write(captions))
    elif output_format == 'sami':
        f.write(SAMIWriter().write(captions))
    elif output_format == 'scc':
        f.write(SCCWriter().write(captions))
    elif output_format == 'srt':
        f.write(SRTWriter().write(captions))
    elif output_format == 'transcript':
        f.write(TranscriptWriter().write(captions))
    elif output_format == 'vtt':
        writer = WebVTTWriter()
        writer.force_write_hours = True

        # If the source file was an SCC file, then apply padding to the caption positions to ensure the captions
        # appear in the safe caption area.
        #if type(reader) is SCCReader:
        #    writer.apply_cea608_padding = True

        f.write(writer.write(captions))

    f.close()

    exit(0)


if __name__ == '__main__':
    main()

