# commit_history.py
"""
	Given the name of a Github repo and the name of its owner, this script outputs information about the average number of commits per week committed to the Github repo 
	in the past.
"""
import requests
import calendar
import argparse
import sys
from unittest.mock import Mock, MagicMock

parser = argparse.ArgumentParser()
parser.add_argument('repo', type=str, help='name of repo to view the commit history of')
parser.add_argument('user', type=str, help='name of owner of the repo')
parser.add_argument('-weeks', type=int, default=52, help='number of weeks of commit history to check')
parser.add_argument('-useList', type=bool, default=False, help='outputs list of weekday commit averages if True, else outputs greatest commit average weekday')
parser.add_argument('-sort', type=str, default='desc', help='order to sort weekday list')
parser.add_argument('-runTests', type=bool, default=False, help='runs tests if True, otherwise functions as normal')
args = parser.parse_args(sys.argv[1:])
repo = args.repo
user = args.user
weeks = args.weeks
sort = args.sort
useList = args.useList
runTests = args.runTests

def greatest_commit_avg_weekday(repo: str, user: str, weeks: int):
	"""
		Given the name of a Github repo, the name of the user who owns the repo, returns the weekday with the greatest average of commits over the past year.
		If weeks is given as an argument, instead checks over the past number of weeks.
	"""
	response_json = requests.get('https://api.github.com/repos/' + user + '/'+ repo + '/stats/commit_activity').json()
	week_totals = [0, 0, 0, 0, 0, 0, 0]
	for week in response_json[52 - weeks:]:
		days = week['days']
		week_totals = [week_totals[i] + days[i] for i in range(7)]

	max_total = max(week_totals)
	greatest_commit_avg_weekday = calendar.day_name[week_totals.index(max_total) - 1]
	return greatest_commit_avg_weekday + ' ' + str(round(max_total/weeks))


def sorted_commit_avg_weekdays(repo: str, user: str, weeks: int, sort: str):
	"""
		Given the name of a Github repo, the name of the user who owns the repo, returns the list of weekdays with their respective average of commits over the past year.
		If weeks is given as an argument, instead checks over the past number of weeks. If sort is given as an argument, determines if the list is sorted in ascending or
		descending order.
	"""
	response_json = requests.get('https://api.github.com/repos/' + user + '/'+ repo + '/stats/commit_activity').json()
	week_totals = [0, 0, 0, 0, 0, 0, 0]
	output = ''
	for week in response_json[52 - weeks:]:
		days = week['days']
		week_totals = [week_totals[i] + days[i] for i in range(7)]

	if sort == 'asc':
		for _ in range(7):
			min_total = min(week_totals)
			min_total_index = week_totals.index(min_total)
			min_weekday = calendar.day_name[min_total_index - 1]
			output += min_weekday + ' ' + str(round(min_total/weeks)) + '\n'
			week_totals[min_total_index] = float('inf')
	else:
		for _ in range(7):
			max_total = max(week_totals)
			max_total_index = week_totals.index(max_total)
			max_weekday = calendar.day_name[max_total_index - 1]
			output += max_weekday + ' ' + str(round(max_total/weeks)) + '\n'
			week_totals[max_total_index] = float('-inf')

	return output

if not runTests:
	if useList:
		print(sorted_commit_avg_weekdays(repo, user, weeks, sort))
	else:
		print(greatest_commit_avg_weekday(repo, user, weeks))


#############################################################################################################################################################################
def run_simple_tests():
	"""
		Simple tests to make sure it calculates the average and the weekday properly.
	"""
	mock = Mock()
	requests.get = mock

	Mock.json = MagicMock(return_value=[{'days':[1, 0, 0, 0, 0, 0, 0]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Sunday 1'

	Mock.json = MagicMock(return_value=[{'days':[0, 1, 0, 0, 0, 0, 0]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Monday 1'

	Mock.json = MagicMock(return_value=[{'days':[0, 0, 1, 0, 0, 0, 0]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Tuesday 1'

	Mock.json = MagicMock(return_value=[{'days':[0, 0, 0, 1, 0, 0, 0]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Wednesday 1'

	Mock.json = MagicMock(return_value=[{'days':[0, 0, 0, 0, 1, 0, 0]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Thursday 1'

	Mock.json = MagicMock(return_value=[{'days':[0, 0, 0, 0, 0, 1, 0]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Friday 1'

	Mock.json = MagicMock(return_value=[{'days':[0, 0, 0, 0, 0, 0, 1]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Saturday 1'

def run_bonus_tests():
	"""
		Tests for Bonus Challenge 1 and Bonus Challenge 2 - changing the amount of weeks we look at, as well as looking at the full week of commit averages.
	"""
	mock = Mock()
	requests.get = mock

	Mock.json = MagicMock(return_value=[{'days':[0, 0, 0, 0, 0, 0, 0]}] * 50 + [{'days':[1, 1, 1, 1, 1, 1, 1]}] + [{'days':[51, 51, 51, 51, 51, 51, 51]}])
	assert greatest_commit_avg_weekday('test', 'test', 1) == 'Sunday 51'
	assert sorted_commit_avg_weekdays('test', 'test', 1, 'desc') == 'Sunday 51\nMonday 51\nTuesday 51\nWednesday 51\nThursday 51\nFriday 51\nSaturday 51\n'
	assert greatest_commit_avg_weekday('test', 'test', 2) == 'Sunday 26'
	assert sorted_commit_avg_weekdays('test', 'test', 2, 'asc') == 'Sunday 26\nMonday 26\nTuesday 26\nWednesday 26\nThursday 26\nFriday 26\nSaturday 26\n'
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Sunday 1'
	assert sorted_commit_avg_weekdays('test', 'test', 52, 'desc') == 'Sunday 1\nMonday 1\nTuesday 1\nWednesday 1\nThursday 1\nFriday 1\nSaturday 1\n'

	Mock.json = MagicMock(return_value=[{'days':[1, 2, 3, 4, 5, 6, 7]}] * 52)
	assert greatest_commit_avg_weekday('test', 'test', 52) == 'Saturday 7'
	assert sorted_commit_avg_weekdays('test', 'test', 52, 'asc') == 'Sunday 1\nMonday 2\nTuesday 3\nWednesday 4\nThursday 5\nFriday 6\nSaturday 7\n'

def test_master():
	"""
		Runs all unit tests. Can be scaled to run more tests.
	"""
	run_simple_tests()
	run_bonus_tests()

if runTests:
	test_master()
