#!/usr/bin/python3

from helpers.jira_helper import LogJira
from helpers.boto3_helper import LogAWS
from scrts import security_groups_ids, usr, pwd, url

jira = LogJira(usr, pwd, url)
c_ticket_num = "REM-6"
c_ticket, is_ok = jira.get_ticket(c_ticket_num)

if not is_ok:
	exit()

print(c_ticket.fields.status)
print(c_ticket.fields.assignee)
description = c_ticket.fields.description
summary = c_ticket.fields.summary
reporter = c_ticket.fields.reporter
ips = jira.extract_ips(description)
print(ips, reporter)
aws = LogAWS()
aws.set_ec2_resource()

security_groups = [
	aws.get_security_group(sgi)
	for sgi in security_groups_ids
]

for ip in ips:
	for security_group in security_groups:
		if (
			("Whitelist IP" == summary) or
			("Abilitazione IP" == summary) or
			("whitelist" in summary) or
			("Whitelist" in summary) or
			("white" in summary and "list" in summary)
		):
			resp = aws.add_ip(ip, security_group, f"{reporter} {c_ticket_num}")
			comment = f"Ciao,\nIP {', '.join(ips)} abilitati\n\nSaluti,\nFederico"
		else:
			resp = aws.rm_ip(ip, security_group)
			comment = f"Ciao,\nIP {', '.join(ips)} disabilitati\n\nSaluti,\nFederico"

		if resp['Return']:
			break

#jira.post_comment(comment, c_ticket_num)
def solve_jira(c_ticket):
	jira.assigne_issue(c_ticket)
	issue, is_ok = jira.get_ticket(c_ticket_num)
	jira.solve_issue(issue, comment)
	c_ticket, is_ok = jira.get_ticket(c_ticket_num)
	print(c_ticket.fields.status)
	print(c_ticket.fields.assignee)

solve_jira(c_ticket)
print(resp)