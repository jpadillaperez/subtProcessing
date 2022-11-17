from io import FileIO as file
import sys
import shutil
import re
import argparse
import os
from googletrans import Translator
from pathlib import Path


def parse_options():
    parser = argparse.ArgumentParser(
        description='Translate srt subtitles.')

    parser.add_argument('-od', '--output_directory',
                        help="output directory with processed subtitles")
                
    parser.add_argument('-o', '--overwrite', action="store_true", default=False,
                        help="overwite original file")

    parser.add_argument('-src', '--source', default='en',
                        help="language of original subtitles (i.e. 'en' for english)")

    parser.add_argument('-dest', '--destination', default='de',
                        help="language of output subtitles (i.e. 'de' for german)")

    return parser.parse_args()

def translate_file(options):
    if not Path.is_dir(Path(options.output_directory)):
        sys.exit("ERROR: output directory doesn't exist")

    for file in os.listdir(Path.cwd()):
        filename = os.fsdecode(file)

        if '.srt' not in filename:
            break

        isNextText = False
        isThisText = False
        translateQuery = ""
        translator = Translator()
        out_filename = os.path.splitext(filename)[0] + '-translated.srt'

        with open(out_filename, 'w', encoding='utf-8') as out:
            with open(filename, 'r', encoding='utf-8') as srt:
                for line in srt.readlines():
                    if isThisText:
                        translateQuery += line.strip()
                        isNextText = True
                        if line.strip() == "":
                            isNextText = False
                            if translateQuery == "":
                                print("WARNING: skipped defect srt file")
                                break
                            result = translator.translate(
                                translateQuery, src="en", dest="de")
                            translateQuery = ""
                            if len(result.text) < 42:
                                out.write(result.text + "\n" + "\n")
                            else:
                                words = result.text.split()
                                center = int(len(words)/2)
                                sentence = '\n'.join(
                                    [' '.join(words[:center]), ' '.join(words[center:])])
                                out.write(sentence + "\n" + "\n")

                    else:
                        match = re.search(
                            r'^(\d+:\d+:\d+,\d+)\s+--\>\s+(\d+:\d+:\d+,\d+)', line)
                        isNextText = False
                        if match:
                            isNextText = True
                        out.write(line)
                    isThisText = isNextText
                    isNextText = False

        if options.overwrite:
            shutil.move(out_filename, filename)
            out_filename = filename

        if options.output_directory:
            shutil.move(out_filename, Path.joinpath(
                Path(options.output_directory), out_filename))

        print("File '" + filename + "' processed")

if __name__ == "__main__":
    print("Started Translation...\n")
    translate_file(parse_options())
    print("\nTranslation completed!\n")
