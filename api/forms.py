from django import forms

class SearchForm(forms.Form):
    start_idx = forms.IntegerField(initial=1, label='시작 인덱스', min_value=1)
    end_idx = forms.IntegerField(initial=1000, label='종료 인덱스', min_value=1)