from django import forms
from django.core.validators import RegexValidator

VALID_PINYIN_ERROR = "Pinyin must specify numeric tones"
CAPITALIZED_PINYIN_ERROR = "Pinyin should not be capitalized unless its a proper name"

class ChinesePhraseForm(forms.Form):
    pinyin = forms.CharField(
        validators=[RegexValidator(regex=r'^(\s*[a-zA-Z]{1,7}[1-5])+\s*$',
                                   code='valid_pinyin',
                                   message=VALID_PINYIN_ERROR,
                                   ),
                    ],
        widget=forms.fields.TextInput(attrs={
                'placeholder': 'update pinyin',
                      'class': 'form-control',
                }))
    english = forms.CharField(
        widget=forms.fields.TextInput(attrs={
                'placeholder': 'add English translation',
                      'class': 'form-control',
                }))
    is_name = forms.BooleanField(
        required=False,
        label='Proper Name',
        )

    def clean(self):
        cleaned_data = super(ChinesePhraseForm, self).clean()
        pinyin  = cleaned_data.get('pinyin')
        if not pinyin:
            return
        is_name = cleaned_data.get('is_name')
        if is_name:
            return
        if pinyin != pinyin.lower():
            raise forms.ValidationError(CAPITALIZED_PINYIN_ERROR, code='capitalized_pinyin')

