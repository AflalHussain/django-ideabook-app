from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Idea, Suggestion
from accounts.models import User, UserFollowing
from django.db.models import Q
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from .forms import PostForm, SuggForm
from django.contrib.auth.decorators import login_required
import pytz
from django.utils import timezone


# Create your views here.
@login_required(login_url='login/')
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
    following_list=UserFollowing.objects.filter(user=request.user)
    flist=list(obj.following_user for obj in following_list)
    flist.append(request.user)
    feed_ideas=Idea.objects.filter(idea_user__in=flist).order_by('-idea_date')
    liked_ideas=[]
    for feed_idea in feed_ideas:
        if feed_idea.idea_likes.filter(id=request.user.id).exists():
            liked_ideas.append(feed_idea.id)
    context = {'form' : form,'feed_ideas':feed_ideas,'liked_ideas':liked_ideas}
    
    return render(request, 'ideabook/feed.html', context)

@login_required(login_url='login/')
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
    sugglist=idea.suggestion_set.all()
    liked_sugg=[]
    for sugg in sugglist:
        if sugg.sugg_likes.filter(id=request.user.id).exists():
            liked_sugg.append(sugg.id)
    
    context = {'form' : form,'idea':idea,'num_likes':num_likes,'is_liked':liked,'liked_sugg':liked_sugg,}
    
    return render(request, 'ideabook/idea.html', context)
    
@login_required(login_url='login/')
def like_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if idea.idea_likes.filter(id=request.user.id).exists():
        idea.idea_likes.remove(request.user)
    else:
        idea.idea_likes.add(request.user)
    idea.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed')+f'#{idea.id}')

@login_required(login_url='login/')
def edit_idea(request,pk):
    idea=Idea.objects.get(pk=pk)
    if idea.idea_user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES,instance=idea)
            if form.is_valid():
                post = form.save(commit=False)
                post.idea_edit_date=timezone.now()
                post.save()
                return HttpResponseRedirect(reverse('idea',args=(pk,)))
            else:
                form = PostForm(instance=idea)
        else:
            form = PostForm(instance=idea)
        context = {'form' : form,'idea':idea,}
        return render(request, 'ideabook/edit_idea.html', context)

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed'))
    
        
@login_required(login_url='login/')
def delete_idea(request, pk):
  # check if post belongs to user
  idea = Idea.objects.get(id=pk)
  if idea.idea_user == request.user:
      idea.delete()
  # remove it from the database
  # redirect back to same page
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed')+f'#{idea.id}')

@login_required(login_url='login/')
def like_sugg(request, pk):
    sugg = get_object_or_404(Suggestion, pk=pk)
    if sugg.sugg_likes.filter(id=request.user.id).exists():
        sugg.sugg_likes.remove(request.user)
    else:
        sugg.sugg_likes.add(request.user)
    sugg.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed')+f'#{sugg.id}')
@login_required(login_url='login/')
def useraccountview(request,pk):
    user=get_object_or_404(User, pk=pk)
    context = {}
    if request.user==user:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.idea_user = request.user 
                post.save()
                return HttpResponseRedirect(reverse('feed'))
        else:
            form = PostForm()
        context['form']=form
    
    feed_ideas=Idea.objects.filter(idea_user=user).order_by('-idea_date')
    is_liked_dict={}
    for feed_idea in feed_ideas:
        is_liked_dict[feed_idea.id]=feed_idea.idea_likes.filter(id=request.user.id).exists()
    context['feed_ideas']=feed_ideas
    context['is_liked_dict']=is_liked_dict
    context['acc_user']=user

    return render(request, 'ideabook/user_account.html', context)

def searchview(request):
    if request.method=='GET':
        query=request.GET.get('q')
        if query is not None:
            lookups= Q(username__icontains=query)
            results=User.objects.filter(lookups).exclude(username=request.user).distinct()

            flist=UserFollowing.objects.filter(user=request.user,following_user__in=results)
            following_list=list(obj.following_user for obj in flist) 
            print(following_list)
            
            
            #if a user presses the submit button without entering anything, in Django, all the rows of the database table are returned
            submitbutton= request.GET.get('submit')

            context={'results':results,'submitbutton':submitbutton,'following_list':following_list}

            return render(request, 'ideabook/search.html', context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed'))

def follow(request, pk):
    follow_user = get_object_or_404(User, pk=pk)
    if UserFollowing.objects.filter(user=request.user,
                             following_user=follow_user).exists():
        UserFollowing.objects.get(user=request.user,
                             following_user=follow_user).delete()
    else:
        UserFollowing.objects.create(user=request.user,
                             following_user=follow_user)
    
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'feed'))