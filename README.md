# JiraAutoAddIP

## Purpose
When you work sometimes you find yourself in doing very very boring & recurring tasks. These tasks often follow the same pattern with the same content changing only some variables. One scenario is for example when you have to add some IPs in a whitelist for allowing them connect to an EC2 instance.

## Automation
The client asks you to whitelist (or remove) some IPs to allow him to connect to an EC2 instance. He opens a Ticket with the Jira platform, with Jira we can configure webhooks when these kinds of events happen. When a new ticket is opened Jira send a request to our webhook & based on the ticket summary he is gonna decide if add (or remove) the ip from the Security Group attached to the EC2 instance through AWS API. Once the operation is made the webhook will reply to the ticket & update the ticket status to Done.

## Security
The biggest concern here is that the webhook add | remove from the whitelist every single ip in the ticket body without any kind of check, that maybe at a human eye could cause concerns. So we here trust the client request at closed eye.

## Made with fun & good libraries

- boto3 (library for using aws api)
- jira (library for using jira api)
- fastapi (for realizing our webhook)

## Installation

1. Clone it
	```bash
	git clone https://github.com/IadRabbit/JiraAutoAddIP.git
	```

2. Create environment
	```bash
	cd JiraAutoAddIP && python3 -m venv .env && source .env/bin/activate
	```

3. Install dependencies
	```bash
	pip3 install -r req.txt
	```

4. check `scrts.py` and modify it with your own settings

5. Create an IAM user with a proper policy that is able to add & remove IP from security group then edit or create `.aws/config` and add a profile with this name it should looks something like this

	```bash
	[profile add_ip]
	aws_access_key_id = AKITHECATISONTHETABgdWFN
	aws_secret_access_key = mlzWISEEYOUlY4gsgtW
	region = eu-central-1
	```
	> [!IMPORTANT]
	> profile name must be `add_ip`

6. Run
	```bash
	uvicorn webhook:app --host 0.0.0.0 --port 8000
	```
	> [!NOTE]
	> If you are in development use --reload, it helps