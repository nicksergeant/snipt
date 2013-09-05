from annoying.decorators import render_to
from jobs.models import Job


@render_to('jobs/jobs.html')
def jobs(request):
    return {
        'jobs': Job.objects.all().order_by('-created')
    }
