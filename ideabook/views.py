from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Idea, Suggestion
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from .forms import PostForm, SuggForm
from django.contrib.auth.decorators import login_required
import datetime


# Create your views here.
@login_required
def feedview(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.idea_user = request.user 
            post.save()
            return HttpResponseRedirect(reverse('feed'))
    else:
        form = PostForm()

    feed_ideas=Idea.objects.order_by('-idea_date')
    is_liked_dict={}
    for feed_idea in feed_ideas:
        is_liked_dict[feed_idea.id]=feed_idea.idea_likes.filter(id=request.user.id).exists()
    context = {'form' : form,'feed_ideas':feed_ideas,'is_liked_dict':is_liked_dict}
    
    return render(request, 'ideabook/feed.html', context)

@login_required
def ideaview(request,pk):
    idea = get_object_or_404(Idea, pk=pk)
    liked = False
    if idea.idea_likes.filter(id=request.user.id).exists():
        liked = True
    num_likes=idea.num_likes
    if request.method == 'POST':
        form = SuggForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sugg_user = request.user
            post.idea=get_object_or_404(Idea, pk=pk)
            post.save()
            return HttpResponseRedirect(reverse('idea',args=(pk,)))
    else:
        form = SuggForm()
    
    context = {'form' : form,'idea':idea,'num_likes':num_likes,'is_liked':liked}
    
    return render(request, 'ideabook/idea.html', context)
    
@login_required
def like_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if idea.idea_likes.filter(id=request.user.id).exists():
        idea.idea_likes.remove(request.user)
    else:
        idea.idea_likes.add(request.user)
    idea.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed')+f'#{idea.id}')

@login_required
def edit_idea(request,pk):
    idea=Idea.objects.get(pk=pk)
    if idea.idea_user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES,instance=idea)
            if form.is_valid():
                post = form.save(commit=False)
                post.idea_edit_date=datetime.datetime.now()
                post.save()
                return HttpResponseRedirect(reverse('idea',args=(pk,)))
            else:
                form = PostForm(instance=idea)
        else:
            form = PostForm(instance=idea)
        context = {'form' : form,'idea':idea,}
    
        return render(request, 'ideabook/edit_idea.html', context)

@login_required
def delete_idea(request, pk):
  # check if post belongs to user
  idea = Idea.objects.get(id=pk)
  if idea.idea_user == request.user:
      idea.delete()
  # remove it from the database
  # redirect back to same page
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed')+f'#{idea.id}')
@login_required
def myaccountview(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.idea_user = request.user 
            post.save()
            return HttpResponseRedirect(reverse('feed'))
    else:
        form = PostForm()

    feed_ideas=Idea.objects.filter(idea_user=request.user).order_by('-idea_date')
    is_liked_dict={}
    for feed_idea in feed_ideas:
        is_liked_dict[feed_idea.id]=feed_idea.idea_likes.filter(id=request.user.id).exists()
    context = {'form' : form,'feed_ideas':feed_ideas,'is_liked_dict':is_liked_dict}

    return render(request, 'ideabook/myaccount.html', context)