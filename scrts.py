#!/usr/bin/python3

pwd = 'YWRtaW4=' # base64 jira password use "https://gchq.github.io/CyberChef/#recipe=To_Base64('A-Za-z0-9%2B/%3D')&input=Y2lhbw"
usr = 'admin' # jira username
url = 'http://localhost:8080' # jira endpoint
from_port = 22 # for security group
to_port = 22 # for security group

security_groups_ids = {
	'REM': (
		'sg-02a2d5e8b87b81a6a',
	)
}