from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables_list=[],
                 sql_query_test="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.tables_list = tables_list
        self.sql_query_test = sql_query_test


    def execute(self, context):
        self.log.info('DataQualityOperator is started')

        redshift = PostgresHook(self.redshift_conn_id)

        for table in self.tables_list:
            sql_stmt = self.sql_query_test.format(table)
            self.log.info(f"Data quality check for table <{table}>, SQL = <{sql_stmt}>")
            records = redshift.get_records(sql_stmt)

            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. Table <{table}> returned no results.")

            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. Table <{table}> contains 0 rows.")

            self.log.info(f"Data quality check for table <{table}> passed with {num_records} records.")

        self.log.info('DataQualityOperator is finished.')
