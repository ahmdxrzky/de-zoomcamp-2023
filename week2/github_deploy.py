from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from etl_web_to_gcs import etl_web_to_gcs

github_block = GitHub.load("github-repo")

github_dep_instance = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name='store-to-github',
    storage=github_block,
    entrypoint="week2/etl_web_to_gcs.py:etl_web_to_gcs"
)

if __name__ == "__main__":
    github_dep_instance.apply()