from pathlib import Path
import sys
import shutil
import re
import datetime
import argparse
import os
from pathlib import Path


def parse_options():
    parser = argparse.ArgumentParser(
        description='Offset srt subtitles.')

    parser.add_argument('offset', type=float,
                        help="offset to be applied to the subtitles")

    parser.add_argument('-od', '--output_directory',
                        help="output directory with processed subtitles")

    parser.add_argument('-o', '--overwrite', action="store_true", default=False,
                        help="overwite original file")

    return parser.parse_args()

def rzeropad(ms):
    ms = str(int(ms))
    while len(ms) < 3:
        ms += "0"
    return ms

def offset_time(offset, time_string):
    ts = time_string.replace(',', ':').split(':')
    ts = [int(x) for x in ts]
    ts = datetime.datetime(1999, 5, 6, ts[0], ts[1], ts[2], ts[3] * 1000)
    delta = datetime.timedelta(seconds=offset)
    ts += delta
    valid = True
    if ts.day<6:
        print("WARNING: ignoring subtitles with negatime timestamp")
        valid = False
    elif ts.year != 1999 or ts.month != 5 or ts.day != 6:
        #Improve next version
        sys.exit("ERROR: invalid offset resulting timestamp overflow")

    return valid, "%s,%s" % (ts.strftime("%H:%M:%S"), rzeropad(ts.microsecond / 1000))


def sync_file(options):
    if not Path.is_dir(Path(options.output_directory)):
        sys.exit("ERROR: output directory doesn't exist")

    for file in os.listdir(Path.cwd()):
        filename = os.fsdecode(file)

        if '.srt' not in filename:
            break
        
        out_filename = os.path.splitext(filename)[0] + '-sync.srt'
        valid = True

        with open(out_filename, 'w', encoding='utf-8') as out:
            with open(filename, 'r', encoding='utf-8') as srt:
                for line in srt.readlines():
                        match = re.search(
                            r'^(\d+:\d+:\d+,\d+)\s+--\>\s+(\d+:\d+:\d+,\d+)', line)
                        if match:
                            valid, init_time = offset_time(options.offset, match.group(1))
                            if not valid:
                                continue
                            _, end_time = offset_time(options.offset, match.group(2))
                            out.write("%s --> %s\n" % (init_time, end_time))
                        elif not valid:
                            continue
                        else: 
                            out.write(line)
                            
        if options.overwrite:
            shutil.move(out_filename, filename)
            out_filename = filename

        if options.output_directory:            
            shutil.move(out_filename , Path.joinpath(
                Path(options.output_directory), out_filename))

        print("File '" + filename + "' processed")


if __name__ == "__main__":
    print("Started synchronization...\n")
    sync_file(parse_options())
    print("\nSynchronization completed!\n")
