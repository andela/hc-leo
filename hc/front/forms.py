from django import forms
from hc.api.models import Channel
from .models import Category, Blog


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


class TimeoutForm(forms.Form):
    timeout = forms.IntegerField(min_value=60, max_value=31104000)
    grace = forms.IntegerField(min_value=60, max_value=31104000)


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)


class CreateCategoryForm(forms.ModelForm):
    '''form to cater for the creation of a category for a blog'''
    class Meta:
        model = Category
        fields = ['name']

class AddBlogPostForm(forms.ModelForm):
    '''Form to cater to the creation of Blog entires'''
    class Meta:
        model = Blog
        fields = ['title', 'body', 'category']