from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from catalog.models import Series,Movie
from common.models import BaseModel
User=get_user_model()

class Favorite(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='favorites')
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,null=True,blank=True)
    series=models.ForeignKey(Series,on_delete=models.CASCADE,nll=True,blank=True)
    
    class Meta:
        unique_together=({"user","movie","series"})