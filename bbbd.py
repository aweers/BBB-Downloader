import argparse
import sys
import os
import configparser

# positional args

parser = argparse.ArgumentParser()

parser.add_argument('-m', '--multiple', action='store_true', 
    help="use .txt file with multiple input links, one per line; saves to directory with increasing filenames")
	
parser.add_argument('-o', '--offset', type=int, default=0,
    help="use offset for filenames")

parser.add_argument('input_link')
	
parser.add_argument('output_name')

args = parser.parse_args()

config = configparser.ConfigParser()
config.read("config.ini")
BASE_URL = config['DEFAULT']['base_url']


def download_meetingId(meetingId, output_file):
	video_filename = "video_{0}.mp4".format(meetingId[-5:])
	audio_filename = "audio_{0}.mp3".format(meetingId[-5:])

	#presentation
	deskshare_link = BASE_URL + meetingId + "/deskshare/deskshare.webm"

	#audio
	webcam_link = BASE_URL + meetingId + "/video/webcams.webm"

	#download presentation
	print("Start download of video file")
	os.system("ffmpeg -hide_banner -an -i {0} {1}".format(deskshare_link, video_filename))

	#download audio
	print("Start download of audio file")
	os.system("ffmpeg -hide_banner -vn -i {0} {1}".format(webcam_link, audio_filename))

	#combine
	print("Combine video and audio file")
	os.system("ffmpeg -hide_banner -i {0} -i {1} -c copy -map 0:v:0 -map 1:a:0 {2}".format(video_filename, audio_filename, output_file))

	#delete temps
	print("Delete temporary files")
	os.remove(video_filename)
	os.remove(audio_filename)




if args.multiple:
	if args.input_link[-4:] != ".txt":
		args.input_link += ".txt"
	if not os.path.isfile(args.input_link):
		sys.exit("Input is not a valid file: {}".format(args.input_link))
	if not os.path.isdir(args.output_name):
		sys.exit("Output is not a valid directory")
else:
	if args.output_name[-4:] != ".mp4":
		args.output_name += ".mp4"

print("###BigBlueButton Downloader###")
print(args.input_link)

if args.multiple:
	counter = args.offset
	with open(args.input_link) as fp: 
		for line in fp:
			if line[0] == "#":
				continue
			substring_start = "meetingId="
			start = line.find(substring_start)
			if start < 0:
				sys.exit("Missing meetingId: {}".format(line))
				
			meetingId = line[start + len(substring_start):].rstrip()
			
			download_meetingId(meetingId, os.path.join(args.output_name, str(counter).zfill(2) + ".mp4"))
			counter += 1
else:
	substring_start = "meetingId="
	start = args.input_link.find(substring_start)
	if start < 0:
		sys.exit("Missing meetingId")
		
	meetingId = args.input_link[start + len(substring_start):]
	
	download_meetingId(meetingId, args.output_name)