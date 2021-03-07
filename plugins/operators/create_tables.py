from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CreateRedshiftTablesOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query_drop_list = "",
                 query_create_list = "",
                 *args, **kwargs):

        super(CreateRedshiftTablesOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query_create_list = query_create_list

    def execute(self, context):

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
                   
        self.log.info("Creating Redshift tables is started")

        for q in self.query_create_list:
            redshift.run(q)

        self.log.info("Creating Redshift tables is finished")


