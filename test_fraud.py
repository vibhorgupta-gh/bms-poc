from fraud.query_checker import checker
from datetime import date

def test_non_malicious():
	role = 0
	user = 0
	timestamp = date.today()
	query = [0,10,21,12]
	transaction = [role, user, timestamp, query]
	assert checker(transaction) == 1

def test_malicious():
	role = 0
	user = 2
	timestamp = date.today()
	query = [0,12,25,13,2,25,40,1,10,46]
	transaction = [role, user, timestamp, query]
	assert checker(transaction) == 0