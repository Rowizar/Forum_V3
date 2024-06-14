import json
import redis
from .models import PageVisit
from django.contrib.auth.models import User

r = redis.Redis(host='redis', port=6379, db=0)

def log_visit(request):
    if request.path not in ['/admin', '/auth', '/login']:
        visit_data = {
            'user': request.user.pk,
            'url': request.build_absolute_uri(),
            'query_params': json.dumps(request.GET),
            'method': request.method,
            'user_agent': request.headers.get('User-Agent', ''),
        }
        r.lpush('page_visits', json.dumps(visit_data))


def save_visits():
    while r.llen('page_visits') > 0:
        visit_data = json.loads(r.rpop('page_visits'))
        user_id = visit_data.get('user')

        user = None
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                print(f"User with id {user_id} not found.")
                continue

        PageVisit.objects.create(
            user=user,
            url=visit_data['url'],
            query_params=visit_data['query_params'],
            method=visit_data['method'],
            user_agent=visit_data['user_agent'],
            os=visit_data.get('os', ''),
            browser=visit_data.get('browser', '')
        )
