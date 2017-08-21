from sys import *
from time import gmtime, strftime
from urllib2 import urlopen


""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*              Audio Parser (Parent Class)            *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

class AudioParser(object):
	
	def __init__(self, HTML_file):
		self._html_file = HTML_file
		self._html_text = self.import_html_text()
		self._audio_list = []


	def import_html_text(self):
		html_text = self.get_html_file().read()
		return html_text


	def setAudioList(self, audio_list):
		self._audio_list = audio_list


	def get_html_file():
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
		urlopen(url) 


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

		
	def parse_for_Audio(self):
		"""
		Here's where the Play.it parser should go. Returns
		a list of all URLs of MP3 files in HTML file.
		"""	
		


""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                      Tests                          *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

if "__name__" == __main__:
	myHTML_file = open("tester.html", 'r')
	parser = PlayItParser(myHTML_file)

	parser.getAudio()
	


