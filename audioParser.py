from sys import *
from time import gmtime, strftime
import urllib2
import os


""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*              Audio Parser (Parent Class)            *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

class AudioParser(object):
	
	def __init__(self, podcast_url, show_name=""):
		self._html_file = urllib2.urlopen(podcast_url)
		self._html_text = ""
		self._audio_list = []
		self._title_list = []

		if show_name != "":
			self._directory = "Audio_Files/" + show_name
		else: 
			self._directory = "Audio_Files"
		
		self._file_listing = []		

		self.set_html_text()
		self._setFileListing()


	def set_html_text(self):
		self._html_text = self.get_html_file().read()
		

	def get_html_text(self):
		return self._html_text		


	def getDirectory(self):
		return self._directory


	def setAudioList(self, audio_list):
		self._audio_list = audio_list


	def get_html_file(self):
		return self._html_file


	def getAudioList(self):
		return self._audio_list


	def setTitleList(self, title_list):
		self._title_list = title_list
	
	
	def getTitleList(self):
		return self._title_list


	def popAudioList(self):
		return self._audio_list.pop()

	
	def popTitleList(self):
		return self._title_list.pop()

	
	def parse_for_audio(self):
		"""
		Let child class handle this
		"""
		pass


	def _setFileListing(self):
		files = getFileList( self.getDirectory() )		
		newfiles = []
		for f in files:
			newfiles.append( f.replace('.mp3', "") )

		print newfiles
		self._file_listing = newfiles

		
	def _getFileListing(self):
		return self._file_listing


	def isDownloaded(self, title):
		"""
		Check if the title is downloaded already
		"""		
		return (title in self._getFileListing())


	def downloadAllAudio(self):
		"""
		Should cycle through audio_list and download
		each URL. Return bool
		"""
		for url in self.getAudioList():
			downloadAudio(url)


	def downloadAudio(self, URL, filename):
		"""
		Downloads Audio at the specified URL
		"""
		response = urllib2.urlopen(URL)
		data = response.read()
		
		with open(filename, 'w') as f:
			f.write(data)
			

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
			title = self.popTitleList()	
			
			if not self.isDownloaded(title):				
				print "About to download: " + title + ".mp3"
				print "From: " + url
			
				# Download the MP3 at the given URL
				self.downloadAudio(url, self.getDirectory() + "/" + title + ".mp3")
				print "Download Successfull! | " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
				print "\n" + "-"*43


""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*              Play.It Parser (Child Class)           *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

class PlayItParser(AudioParser):
	
	def __init__(self, podcast_url, show_name):
		AudioParser.__init__(self, podcast_url, show_name)
		"""
		NOTE: The Directory name SHOULD be here... not in the parent. 
					Need to address.
		"""
		

	def parse_for_audio(self):
		"""
		Here's where the Play.it parser should go. Sets  
		list of all URLs of MP3 files in HTML file.
		"""
		text = self.get_html_text()
		
		starting_key = 'div id="embed-audioplayer-'
		title_key = 'class="title"'
		title_end_key = '</'
		url_key = '<source src="'
		url_end_key = '?'

		title_list = []
		audio_list = []
	
		while (text.find(starting_key) != -1) :
			starting_idx = text.find(starting_key) + len(starting_key)
			text = text[starting_idx:]
			
			title_idx = text.find(title_key) + len(title_key)
			text = text[title_idx:]
			title_end_idx = text.find(title_end_key)
	
			title_list.append( text[1:title_end_idx] )

			url_idx = text.find(url_key) + len(url_key) - 1
			text = text[url_idx:]
			url_end_idx = text.find(url_end_key)
			
			audio_list.append( text[1:url_end_idx] )	
			
		# Reverse the list - need in chronological order
		audio_list.reverse()
		title_list.reverse()
		
		self.setAudioList( audio_list)
		self.setTitleList( title_list)



""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                Helper Functions                     *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

def getFileList(relative_directory = ""):
	mypath = os.getcwd() + "/" + relative_directory
	
	return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]





""" * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                      Tests                          *
* * * * * * * * * * * * * * * * * * * * * * * * * * """

if __name__ == "__main__":
	
	#felger_and_mazz_url = 'http://www1.play.it/audio/felger-massarotti/'
	#parser = PlayItParser(felger_and_mazz_url, "Felger_and_Mazz")

	#zolak_and_bertrand_url = 'http://www1.play.it/audio/zolak-bertrand/'
	#parser = PlayItParser(zolak_and_bertrand_url, "Zolak_and_Bertrand")

	toucher_and_rich_url = 'http://www1.play.it/audio/toucher-rich/'
	parser = PlayItParser(toucher_and_rich_url, "Toucher_and_Rich")	

	# Get Aduio Test
	parser.getAudio()
		

	# Parsing Test
	"""
	parser.parse_for_audio()
	print "Number of URLs: " + str(len(parser.getAudioList()))
	print "List of URLs:"
	for url in parser.getAudioList():
		print url

	print "Number of Titles: " + str(len(parser.getTitleList()))
	print "List of Titles: "
	for title in parser.getTitleList():
		print title
	"""

	# Check Directory Test
	"""
	parser._setFileListing()
	for f in parser._getFileListing():
		print f

	print "----------------------------"
	testlist = ["something", "blah", "Tom Brady", "Patriots"]
	for tester in testlist:
		print tester + " in list: " + str( parser.isDownloaded(tester) )
	"""
