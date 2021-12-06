from django.shortcuts import render, redirect

from MainApp.forms import EntryForm, TopicForm
from .models import Topic, Entry

from django.contrib.auth.decorators import login_required

from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'MainApp/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #key is used in html, value is used in the view function
    context = {'topics':topics}
    return render(request, 'MainApp/topics.html', context)
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.all()
    context = {"topic":topic, 'entries':entries}
    return render(request, "MainApp/topic.html", context)
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainApp:topics')
    #context is a dictionary that helps us pass data
    context = {'form':form}
    return render(request, 'MainApp/new_topic.html', context)
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form =EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()

            return redirect('MainApp:topic', topic_id=topic_id )
    context = {'form':form, 'topic':topic}
    return render(request, 'MainApp/new_entry.html', context)
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('MainApp:entry', topic_id = topic.id)
    
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'MainApp/edit_entry.html', context)


