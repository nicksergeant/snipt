from annoying.decorators import ajax_request, render_to
from jobs.models import Job

import json


@render_to('jobs/jobs.html')
def jobs(request):
    return {}


@ajax_request
def jobs_json(request):

    jobs_json = []

    jobs = Job.objects.all().order_by('-created')

    for job in jobs:
        jobs_json.append(json.loads(job.data))

    return jobs_json
