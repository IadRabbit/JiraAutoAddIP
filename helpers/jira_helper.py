#!/usr/bin/python3

from re import findall
from jira.client import JIRA
from base64 import b64decode
from ipaddress import ip_address
from jira.resources import Issue
from jira.exceptions import JIRAError

class LogJira:
	def __init__(self, usr: str, pwd: str, url: str) -> None:
		self.__login(usr, pwd, url)

	def __login(self, usr, pwd, url):
		self.__jira = JIRA(
			server = url,
			auth = (
				usr, b64decode(pwd).decode()
			)
		)

		self.__account_id = self.__jira.myself()['name']

		self.__default_assignee = {
			"name": self.__account_id
		}

	def get_ticket(self, ticket: str) -> tuple[Issue, bool]:
		try:
			ticket = self.__jira.issue(ticket)

			return ticket, True
		except JIRAError as err:
			return err.text, False

	@staticmethod
	def extract_ips2(description: str) -> list[str]:
		ips = []

		for line in description.split("\r"):
			c_line = (
				line
				.replace("\r", "")
				.replace("\n", "")
			)

			try:
				ip_address(c_line)
				ips.append(c_line)
			except ValueError:
				pass

		return ips

	@staticmethod
	def extract_ips(description: str) -> list[str]:
		ips = findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", description)

		ips = list(
			dict.fromkeys(ips)
		) #cause somebody put ip like urls

		return ips

	def post_comment(
		self,
		comment: str,
		ticket_num: int
	) -> None:
		self.__jira.add_comment(ticket_num, comment)

	def assigne_issue(self, issue: Issue) -> None:
		issue.update(assignee = self.__default_assignee)

	def solve_issue(
		self,
		issue: Issue,
	) -> None | JIRAError:
		#self.__jira.transition_issue(issue, transition = "Assign")
		#self.__jira.transition_issue(issue, transition = "In progress")

		try:
			self.__jira.transition_issue(
				issue,
				transition = "Done"
			)
		except JIRAError as err:
			return err