import boto3
from pathlib import Path
import json
import time
import logging
from glacier.constants import INVENTORY_IDS

LOG = logging.getLogger(__name__)


class Glacier:
    def __init__(self, vault_name: str = None, output_format: str = "zip"):
        self.client = boto3.resource("glacier")
        self.account_id = boto3.client("sts").get_caller_identity().get("Account")
        self.vault_name = vault_name
        self.output_format = output_format
        if vault_name:
            self.retrieve_inventory_id = INVENTORY_IDS.get(vault_name)
            vault_path = Path("vaults") / vault_name
            self.inventory_output_path = vault_path / "inventory-output.json"
            self.archive_job_ids_path = vault_path / "archive-job-ids.json"
            self.archive_data = vault_path / "data"

    def init_vault_folder(self):
        response = boto3.client("glacier").list_vaults()
        vault_names = [vault.get("VaultName") for vault in response.get("VaultList")]
        LOG.info(vault_names)
        for vault_name in vault_names:
            Path(f"vaults/{vault_name}/data/").mkdir(parents=True, exist_ok=True)

    def retrieve_inventory(self):
        job = self.client.Job(
            self.account_id, self.vault_name, self.retrieve_inventory_id
        )
        response = job.get_output()
        LOG.info(response)
        with open(self.inventory_output_path, "wb") as f:
            f.write(response["body"].read())

    def init_inventory_job(self):
        output = boto3.client("glacier").initiate_job(
            vaultName=self.vault_name, jobParameters={"Type": "inventory-retrieval"}
        )
        LOG.debug(output)
        job_id = output.get("jobId")
        LOG.info(job_id)

    def init_archive_job(self):
        if Path(self.archive_job_ids_path).exists():
            LOG.info("Archive Retrieval job is already initialized")
            return
        with open(self.inventory_output_path, "r") as f:
            output = json.loads(f.read())
            archive_ids = [item.get("ArchiveId") for item in output.get("ArchiveList")]

        archive_job_ids = list()
        for archive_id in archive_ids:
            job_params = {
                "Type": "archive-retrieval",
                "ArchiveId": archive_id,
                "Tier": "Expedited",
            }
            response = boto3.client("glacier").initiate_job(
                vaultName=self.vault_name, jobParameters=job_params
            )
            archive_job_ids.append(response.get("jobId"))

        with open(self.archive_job_ids_path, "w") as f:
            f.write(json.dumps({"JobIds": archive_job_ids}))
        LOG.info("Archive Retrieval job is initialized")

    def retrieve_archive(self):
        with open(self.archive_job_ids_path, "r") as f:
            output = json.loads(f.read())
            job_ids = output.get("JobIds")

        for job_id in job_ids:
            job = self.client.Job(self.account_id, self.vault_name, job_id)
            while not job.completed:
                LOG.info(f"{job.job_id} is not ready yet. Sleeping for 60 seconds...")
                time.sleep(60)
                job = self.client.Job(self.account_id, self.vault_name, job_id)
            response = job.get_output()
            LOG.info(f"Downloading {job.job_id}")
            with open(
                self.archive_data / f"{str(time.time())}.{self.output_format}", "wb"
            ) as f:
                f.write(response["body"].read())
            LOG.info(f"Downloaded {job.job_id}")

    def is_archive_jobs_completed(self):
        with open(self.archive_job_ids_path, "r") as f:
            output = json.loads(f.read())
            job_ids = output.get("JobIds")

        for job_id in job_ids:
            job = self.client.Job(self.account_id, self.vault_name, job_id)
            LOG.info(job.completed)
