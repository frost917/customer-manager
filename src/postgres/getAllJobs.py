
def getJobsDict(self, UUID):
    try:
        self.cur.execute("""
    SELECT 
        customer.customer_id,
        customer.customer_name,
        customer.phone_number,
        visit_history.job_id,
        visit_history.visit_date,
        job_list.jobs_finish,
        job_history.job_price,
        job_history.job_description
    FROM customer
    INNER JOIN visit_history
    ON ( customer.customer_id = visit_history.customer_id )
    INNER JOIN job_list
    ON ( visit_history.job_id = job_list.job_id )
    INNER JOIN job_history
    ON ( visit_history.job_id = job_history.job_id )
    WHERE customer.is_deleted = False AND customer.user_id = %s
    """, (UUID,))
    
        return dict(self.cur.fetchall())
    except:
        return None