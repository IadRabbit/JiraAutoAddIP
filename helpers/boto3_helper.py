#!/usr/bin/python3

from typing import Any
from boto3 import Session
from botocore.exceptions import ClientError

class LogAWS:
	def __init__(
		self,
		aws_access_key_id: str | None = None, 
		aws_secret_access_key: str | None = None,
		region_name: str | None = None
	) -> None:

		self.login(
			aws_access_key_id, aws_secret_access_key, region_name
		)

	def login(
		self,
		aws_access_key_id: str | None = None, 
		aws_secret_access_key: str | None = None,
		region_name: str | None = None
	) -> None:

		if aws_access_key_id and aws_secret_access_key and region_name:
			self.__aws = Session(
				region_name = region_name,
				aws_access_key_id = aws_access_key_id,
				aws_secret_access_key = aws_secret_access_key
			)
		else:
			self.__aws = Session(
				profile_name = 'add_ip',
			)

	def set_ec2_resource(self) -> None:
		self.__ec2_resource = self.__aws.resource("ec2")

	def get_security_group(self, sgi) -> None:
		return self.__ec2_resource.SecurityGroup(sgi)

	@staticmethod
	def __generate_body_ips_authorize(
		ips: list[str],
		description: str = '',
		from_port: int = 22,
		to_port: int = 22
	) -> list[dict]:

		body_data = [
			{
				"FromPort": from_port,
				"IpProtocol": "tcp",
				"IpRanges": [
					{
						"CidrIp": f"{ip}/32",
						"Description": description
					}
				],
				"ToPort": to_port
			}
			for ip in ips
		]

		return body_data

	@staticmethod
	def __generate_body_ips_revoke(
		ips: list[str],
		from_port: int = 22,
		to_port: int = 22
	) -> list[dict]:
		body_data = [
			{
				"FromPort": from_port,
				"IpProtocol": "tcp",
				"IpRanges": [
					{
						"CidrIp": f"{ip}/32"
					}
				],
				"ToPort": to_port
			}
			for ip in ips
		]

		return body_data

	def add_ip(
		self,
		ip: str,
		sg: str,
		description: str = '',
		from_port: int = 22,
		to_port: int = 22
	):
		return self.add_ips(
			[ip], sg, description,
			from_port, to_port
		)

	def add_ips(
		self,
		ips: list[str],
		sg: str,
		description: str = '',
		from_port: int = 22,
		to_port: int = 22
	):
		data = self.__generate_body_ips_authorize(
			ips, description, from_port, to_port
		)

		try:
			resp = sg.authorize_ingress(IpPermissions = data)
		except ClientError as err:
			resp = {
				"Return": False,
				"err": err
			}

		return resp

	def rm_ip(
		self,
		ip: str,
		sg: str,
		from_port: int = 22,
		to_port: int = 22
	):
		return self.rm_ips(
			[ip], sg, from_port, to_port
		)

	def rm_ips(
		self,
		ips: list[str],
		sg: str,
		from_port: int = 22,
		to_port: int = 22
	) -> dict[str, bool | ClientError | Any]:

		data = self.__generate_body_ips_revoke(
			ips, from_port, to_port
		)

		try:
			resp = sg.revoke_ingress(IpPermissions = data)
		except ClientError as err:
			resp = {
				"Return": False,
				"err": err
			}

		return resp