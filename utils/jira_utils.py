from helpers.jira_helper import LogJira
from helpers.boto3_helper import LogAWS

from utils.logger_utils import webhook_logger

from scrts import (
	usr, pwd, url,
	security_groups_ids, from_port, to_port
)

jira = LogJira(usr, pwd, url)
aws = LogAWS()
aws.set_ec2_resource()

def add_or_del(summary: str):
	add = False

	if 'whitelist' in summary.lower():
		add = True

	return add

def solve_ticket_ips(ticket_id: str) -> None:
	c_ticket, exist = jira.get_ticket(ticket_id)

	if not exist:
		webhook_logger.warning(f'No Jira Ticket \'{ticket_id}\'')
		return

	project = c_ticket.fields.project.__str__()
	print(project)

	if not project in security_groups_ids:
		webhook_logger.warning(f'This project \'{project}\' doesn\'t have any security group set up')
		return

	description = c_ticket.fields.description
	summary = c_ticket.fields.summary
	reporter = c_ticket.fields.reporter
	ips = jira.extract_ips(description)

	webhook_logger.info('Ticket INFO')
	#webhook_logger.info(f'Description: {description}')
	webhook_logger.info(f'Summary: {summary}')
	webhook_logger.info(f'Reporter: {reporter}')
	webhook_logger.info(f'IPs: {ips}')

	is_add = add_or_del(summary)

	msg = 'removed from'
	comment = f"Hi,\nIP {', '.join(ips)} revoked"

	if is_add:
		msg = 'added to'
		comment = f"Hi,\nIP {', '.join(ips)} added"

	for ip in ips:
		for security_group in security_groups_ids[project]:
			security_group = aws.get_security_group(security_group)

			if is_add:
				resp = aws.add_ip(
					ip, security_group,
					description = f'{reporter} - {ticket_id}',
					from_port = from_port,
					to_port = to_port
				)

			else:
				resp = aws.rm_ip(
					ip, security_group,
					from_port = from_port,
					to_port = to_port
				)

			if resp['Return']:
				webhook_logger.info(f'IP \'{ip}\' {msg} Security Group \'{security_group.id}\'')
				break
			else:
				webhook_logger.warning(resp['err'].response['Error']['Message'])

	jira.assigne_issue(c_ticket)
	c_ticket.update(comment = comment)
	is_ok = jira.solve_issue(c_ticket)
	#status_ticket = c_ticket.fields.status

	if is_ok is None:
		webhook_logger.info(f'Ticket \'{ticket_id}\' is Done')
	else:
		webhook_logger.warning(f'Ticket \'{ticket_id}\' need attention. {is_ok.text}')