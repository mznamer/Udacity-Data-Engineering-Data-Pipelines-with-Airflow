from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadOperator(BaseOperator):

    sql_delete = "DELETE FROM {}"
    sql_insert = "INSERT INTO {} {}"

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 destination_table="",
                 sql_query="",
                 flag_clear_table = False,
                 *args, **kwargs):

        super(LoadOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.destination_table = destination_table
        self.sql_query = sql_query
        self.flag_clear_table = flag_clear_table


    def execute(self, context):

        self.log.info(f"LoadOperator for {self.destination_table} is started")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.flag_clear_table:
            self.log.info(f"Clearing data from {self.destination_table} Redshift table")
            sql_stmt = self.sql_delete.format(self.destination_table)
            redshift.run(sql_stmt)

        self.log.info(f"Inserting data in {self.destination_table}")
        sql_stmt = self.sql_insert.format(self.destination_table, self.sql_query)
        redshift.run(sql_stmt)

        self.log.info(f"LoadOperator for {self.destination_table} is finished")
