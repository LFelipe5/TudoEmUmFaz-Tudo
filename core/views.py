import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ScrapeForm, TaskForm
from .models import Task
from .scraper import scrape


@login_required
def home(request):
    return render(request, 'core/home.html', {'open_tasks': Task.objects.filter(owner=request.user, completed=False).count()})


@login_required
def tasks(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.save()
        return redirect('tasks')
    return render(request, 'core/tasks.html', {'form': form, 'tasks': Task.objects.filter(owner=request.user)})


@login_required
@require_POST
def task_action(request, pk, action):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if action == 'delete':
        task.delete()
    elif action == 'toggle':
        task.completed = not task.completed
        task.save(update_fields=['completed'])
    return redirect('tasks')


@login_required
def scraper(request):
    form = ScrapeForm(request.POST or None)
    result = None
    if request.method == 'POST' and form.is_valid():
        try:
            result = scrape(form.cleaned_data['url'])
        except (ValueError, OSError, requests.RequestException):
            form.add_error('url', 'Could not read this page. Use a reachable public HTML URL (up to 1 MB).')
    return render(request, 'core/scraper.html', {'form': form, 'result': result})
