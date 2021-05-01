from django import forms
from .models import Posts
from .models import Photo


class CreatePost(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['b_locType1', 'b_locType2', 'b_locType3',
                  'b_title', 'b_text']

class CreatePhoto(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

