from apscheduler.schedulers.background import BackgroundScheduler

from cron.lend_funding_job import LendFundingJob

scheduler = BackgroundScheduler()

lend_funding_job = LendFundingJob()


def start_all():
    scheduler.add_job(func=lend_funding_job.lend, trigger="interval", seconds=25 * 60)
    scheduler.start()