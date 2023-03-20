from googletrans import Translator
# import temp1

def translate(t):
	translator = Translator()

	# Define the text to be translated
	text = t

	# Translate the text to Hindi
	result = translator.translate(text, src='en', dest='hi')

	# Print the translated text

	# print(result.text)
	return result.text