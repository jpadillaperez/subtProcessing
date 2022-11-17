# subtProcessing
Tool for stl subtitle batch processing to synchronize and/or translate to/from any language.

## Usage
Open a console in the folder that contains all the stl files.

For synchronizing subtitles, specify the time offset in seconds as a float
 ```
 sync_subs -od path\to\output\directory 1.0
 ```
 or alternatively overwrite the stl files
 ```
 sync_subs -o 1.0
 ```
 For translating subtitles
 ```
 translate_subs -od path\to\output\directory
 ```
 or alternatively overwrite the stl files and/or specify the source and destination language (english->german by default):
 ```
 translate_subs -o -src es -dest ro
 ```
