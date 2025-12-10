from django.forms import ModelForm

from comments.models import Comments


class AddCommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_text']



