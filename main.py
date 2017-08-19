import pandas as pd

from scipy.stats import hypergeom
from collections import OrderedDict

def term_frequency_matrix(dframe, label_column, text_column, stop_words=None):
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
	for category, subpopulation in dframe.groupby(label_column):

		term_frequency[category] = OrderedDict()
		for element in subpopulation[text_column]:
			if type(element) is str:
				tokenized = element.split(' ')
			else:
				tokenized = element

			for word in tokenized:
				word = word.strip()
				if word in stop_words:
					continue
				if word in term_frequency[category]:
					term_frequency[category][word] += 1
				else:
					term_frequency[category][word] = 1

	return pd.DataFrame.from_dict(term_frequency)

def fisher_exact(word, category, term_frequency_matrix, threshold=.05, stop_words=None):
	"""Determines if distribution of word in subpopulation 'category' 
	is sufficiently different than aggregate populations distribution

	Parameters
	__________ 

	word : type str 
		row of dataframe. word whose predictive value is being determined 

	category : type str 
		column of dataframe. subpopulation that presence of 'word' may or may not predict 

	dframe : type pandas.DataFrame 
		dataframe of 	
	"""
	num_catagory = 
	num_word_in_category = term_frequency_matrix.loc[word, category]
	# TODO : figure out how to get this working
	# num_word_in_aggregate = term_frequency_matrix.loc[word].apply()
	

def predictive_words(dframe, stop_words):
	tf = term_frequency_matrix(dframe, stop_words)

if __name__=='__main__':
	data = pd.read_table('~/Desktop/smsspamcollection/SMSSpamCollection', header=None)
	data.columns = ['label','text']
	tf = term_frequency_matrix(data, 'label', 'text')
	# print tf['ham']
	fisher_exact('"HELLO"', 'ham', tf)