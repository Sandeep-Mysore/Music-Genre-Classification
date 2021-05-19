#!/usr/bin/env python
import sys
import os
import sox

#from pydub import AudioSegment


genre_dirs = ['/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/Carnatic/Adana','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Alhiya','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Bahar',
'/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Behag','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Chandra','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Des','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Durga',
'/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Gaud','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/JaunaPuri','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Pahadi','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Peelu','/Users/sandeepmysore/Desktop/Academic/Course/Sem_8/Minor/Dataset/genres/Tilang'
]

for genre_dir in genre_dirs:

	os.chdir(genre_dir)

	print('Contents of ' + genre_dir + ' before conversion: ')

	os.system("ls")

	for file in os.listdir(genre_dir):
		# SOX
		#song = AudioSegment.from_file(file)
		#song.export(path[:-3] + "wav", format='wav')

		os.system("sox " + str(file) + " " + str(file[:-4]) + ".wav")
		#os.system("sox -t auto" + str(file) + " -e signed-integer " + str(file[:-3]) + ".wav")


	#os.system("rm *.mid")

	print('After conversion:')

	os.system("ls")

	print('\n')

print("Conversion complete.")