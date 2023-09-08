from utils.logger_utils import webhook_logger

from fastapi import FastAPI
from uvicorn import run as run_server

from utils.jira_utils import solve_ticket_ips as solve_ticket_jira_ips

app = FastAPI()

@app.post("/solve_ticket_jira_ip/{ticket_id}")
async def solve_ticket(ticket_id: str):
	webhook_logger.info(f'Received Ticket \'{ticket_id}\'')

	solve_ticket_jira_ips(ticket_id)

	return 'DONE'

if __name__ == "__main__":
	run_server(
		app,
		host = "0.0.0.0",
		port = 8000
	)