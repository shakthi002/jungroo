import nltk
from nltk.corpus import wordnet

# Download the WordNet corpus if it's not already downloaded
nltk.download('wordnet')

# Define a word to check
def check(word):
# word = "bank"

	# Get the synsets (sets of synonyms) for the word from WordNet
	synsets = wordnet.synsets(word)

	# Print the definitions for each synset
	count=0
	for synset in synsets:
		# print(f"Definition ({synset.name()}): {synset.definition()}")
		count+=1
	if count>0:
		return 1
	else:
		return 0
