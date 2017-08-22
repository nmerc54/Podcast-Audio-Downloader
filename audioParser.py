from sys import *
from time import gmtime, strftime
from urllib2 import urlopen


""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*              Audio Parser (Parent Class)            *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

class AudioParser(object):
	
	def __init__(self, HTML_file):
		self._html_file = HTML_file
		self._html_text = ""
		self._audio_list = []

		self.set_html_text()


	def set_html_text(self):
		self._html_text = self.get_html_file().read()
		

	def get_html_text(self):
		return self._html_text		

	def setAudioList(self, audio_list):
		self._audio_list = audio_list


	def get_html_file(self):
		return self._html_file


	def getAudioList(self):
		return self._audio_list

	
	def popAudioList(self):
		return self._audio_list.pop()


	def parse_for_audio(self):
		"""
		Let child class handle this
		"""
		pass


	def downloadAllAudio(self):
		"""
		Should cycle through audio_list and download
		each URL.
		"""
		for url in self.getAudioList():
			downloadAudio(url)


	def downloadAudio(self, URL):
		"""
		Downloads Audio at the specified URL
		"""
		#urlopen(url) 
		print "I'm downloading!"	


	def getAllAudio(self):
		self.parse_for_audio()		# Gather all URLs to be downloaded
		self.downloadAllAudio()		# Download MP3 files at specified URLs


	def getAudio(self):
		"""
		Cycles through URL list. Pops each element off and 
		provides a status update for the user after each 
		download.
		"""
		self.parse_for_audio()	# Gather all URLs to be downloaded

		print "Audio List: " + str(self.getAudioList())
	
		while len(self.getAudioList()) > 0:

			# pop last url off of list
			url = self.popAudioList()					
			print "About to download: " + url
			
			# Download the MP3 at the given URL
			self.downloadAudio(url)						
			print "Download Successfull! | " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) 



""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*              Play.It Parser (Child Class)           *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

class PlayItParser(AudioParser):
	
	def __init__(self, HTML_file):
		AudioParser.__init__(self, HTML_file)

		
	def parse_for_audio(self):
		"""
		Here's where the Play.it parser should go. Sets  
		list of all URLs of MP3 files in HTML file.
		"""	
		text = self.get_html_text()
		
		starting_key = 'div id="embed-audioplayer-'
		title_key = 'class="title"'
		title_end_key = '</'

		title_list = []
		audio_list = []
	
		while text.find(starting_key) != -1 :
			starting_idx = text.find(starting_key) + len(starting_key)
			text = text[starting_idx:]
			\
			title_idx = text.find(title_key) + len(title_key)
			text = text[title_idx:]
			title_end_idx = text.find(title_end_key)
	
			title_list.append( text[0:title_end_idx] )


		self.setAudioList( audio_list )
		#self.setTitleList( title_list )


""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                      Tests                          *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

if __name__ == "__main__":
	myHTML_file = open("tester.html", 'r')
	parser = PlayItParser(myHTML_file)

	# Get Aduio Test
	#parser.getAudio()
	
	# Parsing Test
	parser.parse_for_audio()
	print "Number of URLs: " + str(len(parser.getAudioList()))
	print "List of URLs:"
	for url in parser.getAudioList():
		print url





