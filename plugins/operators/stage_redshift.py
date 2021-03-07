from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):

    template_fields = ("s3_key",)

    copy_to_redshift_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON '{}';
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 destination_table="",
                 s3_bucket="",
                 s3_key="",
                 json_path="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id

        self.destination_table = destination_table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path


    def execute(self, context):

        self.log.info(f"StageToRedshiftOperator for {self.destination_table} is started")

        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Clearing data from {self.destination_table} Redshift table")
        
        sql_stmt = "DELETE FROM {}".format(self.destination_table)
        redshift.run(sql_stmt)

        self.log.info(f"Copying data from S3 {self.s3_key} to Redshift to {self.destination_table}")

        rendered_key = self.s3_key.format(**context)
        s3_path = "{}/{}".format(self.s3_bucket, rendered_key)

        sql_stmt = self.copy_to_redshift_sql.format(
            self.destination_table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.json_path
        )
        redshift.run(sql_stmt)

        self.log.info(f"StageToRedshiftOperator for {self.destination_table} is finished")

