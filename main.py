import pandas as pd

from collections import OrderedDict

def term_frequency_matrix(dframe, stop_words=None):
	"""
	Parameters
	__________

	dframe : type pandas.DataFrame 
		columns are categories, rows are observations

	stop_words : iterable
		list/array/set of words to be ignored by algorithm

	Returns
	_______ 

	_ : type
		term_frequency matrix as dataframe
	"""

	if not isinstance(dframe, pd.DataFrame):
		raise TypeError('input must be pandas.DataFrame')

	if not stop_words:
		stop_words = []

	term_frequency = OrderedDict()
	for category in dframe.columns:
		
		term_frequency[category] = OrderedDict()
		for element in dframe[category]:
			
			if type(element) is str:
				tokenized = element.split(' ')
			else:
				tokenized = element

			for word in tokenized:
				if word in stop_words:
					continue
				if word in term_frequency[category]:
					term_frequency[category][word] += 1
				else:
					term_frequency[category][word] = 1

	return pd.DataFrame(term_frequency)

def hypergeometric(word, dframe, stop_words=None):
	pass

def predictive_words(dframe, stop_words):
	pass

if __name__=='__main__':
	ham = ['the boy bought the basketball', "hey what's up" ]
	spam = ['NEW BUY NOW', 'XXX XXX XXX']

	DATA = pd.DataFrame({'ham' : ham , 'spam' : spam})
	print term_frequency_matrix(DATA)