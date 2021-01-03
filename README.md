# BBB-Downloader
Downloader for BigBlueButton recordings

## Requirements
* ffmpeg needs to be added to the PATH variable.

## Parameters
```console
$ python bbbd.py --help
usage: bbbd.py [-h] [-m] [-o OFFSET] input_link output_name

positional arguments:
  input_link            url for single download, filename for multiple downloads
  output_name           filename for single download, directory for multiple

optional arguments:
  -h, --help            show this help message and exit
  -m, --multiple        use .txt file with multiple input links, one per line;
                        saves to directory with increasing filenames
  -o OFFSET, --offset OFFSET
                        use offset for filenames
```

## Multiple downloads
It is possible to let the program download a list of recordings. Just put the urls you 
want to download in a .txt file and pass it as an argument with the -m option to the 
program call. 
Note that lines starting with a hash sign will be treated as comment. 

## Usage
* Download single recording to file video.mp4:
  ```console
    python bbbd.py bbb.server.de/presentation/meeting_id video.mp4
  ```
* Download multiple files specified in list.txt to directory C:/videos starting with 00.mp4:
  ```console
    python bbbd.py -m list.txt C:/videos
  ```
* Download multiple files specified in list.txt to directory C:/videos starting with 04.mp4:
  ```console
    python bbbd.py -m -o 4 list.txt C:/videos
  ```
