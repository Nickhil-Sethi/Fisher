import numpy as np
import pandas as pd

from scipy.stats import hypergeom
from collections import OrderedDict

import time

def term_frequency_matrix(dframe, label_column, text_column, stop_words=None, frequency_threshold=None):
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
		term_frequency matrix as dataframe"""

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

	data = pd.DataFrame.from_dict(term_frequency)
	data.fillna(0, inplace=True)
	return data

def fisher_exact(word, category, term_frequency_matrix, stop_words=None):
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
	num_word_in_category = float(term_frequency_matrix.loc[word, category])
	num_without_word_in_category = float(term_frequency_matrix.loc[:, category].sum() - num_word_in_category)

	num_word_in_aggregate = float(term_frequency_matrix.loc[word, :].sum())
	# TODO : generalize this
	num_without_word_in_aggregate = float(term_frequency_matrix.loc[:,'ham'].sum() + term_frequency_matrix.loc[:,'spam'].sum() - num_word_in_aggregate)

	rv = hypergeom(num_word_in_aggregate + num_without_word_in_aggregate, num_word_in_category + num_without_word_in_category, num_word_in_aggregate)
	return rv.pmf(num_word_in_category)

def predictive_words(dframe, label, text, threshold=.1, stop_words=None):
	pred_ = OrderedDict()
	tf = term_frequency_matrix(dframe, label, text, stop_words)
	for col in tf.columns:
		pred_[col] = OrderedDict()
		for word in tf.index:
			power = fisher_exact(word, col, tf)
			if 0. < power < threshold:
				pred_[col][word] = power
				print word, col, pred_[col][word]
				time.sleep(.1)


if __name__=='__main__':
	data = pd.read_table('/Users/nickhilsethi/Desktop/smsspamcollection/SMSSpamCollection', header=None)
	data.columns = ['CLASS', 'CONTENT']
	# print data
	data.applymap(lambda x : x.strip() if type(x) is str else x)
	# tf = term_frequency_matrix(data, 'CLASS', 'CONTENT')
	# print tf

	# print fisher_exact('!', 'ham', tf)
	predictive_words(data, 'CLASS', 'CONTENT')


