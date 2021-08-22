from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Idea(models.Model):
    idea_text = models.CharField(max_length=500)
    idea_date=models.DateTimeField('date idea posted',auto_now_add=True)
    idea_edit_date=models.DateTimeField('date idea edited',blank=True,null=True,default=None)
    idea_user=models.ForeignKey(User, related_name='idea_user',on_delete=models.CASCADE)
    idea_likes=models.ManyToManyField(User, related_name='likers', verbose_name=("people who liked"),default=None,blank=True)

    def __str__(self):
        return str(self.idea_text)

    @property   
    def num_likes(self):
        return self.idea_likes.all().count()

    
    

class Suggestion(models.Model):
    sugg_text=models.CharField(max_length=300)
    idea=models.ForeignKey(Idea, on_delete=models.CASCADE)
    sugg_user=models.ForeignKey(User, related_name='sugg',on_delete=models.CASCADE)
    sugg_likes=models.ManyToManyField(User, related_name='sugg_likers', verbose_name=("people who liked"),default=None,blank=True)
    sugg_date=models.DateTimeField('date sugg posted',auto_now_add=True)
    
    @property   
    def num_likes(self):
        return self.sugg_likes.all().count()