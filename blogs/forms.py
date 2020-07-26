from django import forms
from .models import Blogs
from ckeditor.widgets import CKEditorWidget

class BlogCreateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blogs
        fields = ['title','author','image','body']


    def __init__(self,*args,**kwargs):
        super(BlogCreateForm,self).__init__(*args,**kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class':'form-control'})

        self.fields['author'].widget.attrs.update({'style': 'display:none;'})
        self.fields['author'].label = ''


class BlogsForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blogs
        fields = ['title', 'image', 'body']
        required = {
                'author': False
            }

    def __init__(self, *args, **kwargs):
        super(BlogsForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True, *args, **kwargs):
        obj = super(BlogsForm, self).save(commit=False, *args, **kwargs)
        from django.utils.text import slugify
        obj.slug = slugify(obj.title)
        if commit:
            obj.save()
        return obj


