from django import forms

from .models import ChurchRecord,Service

class ChurchRecordForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),required=True)
        
    def __init__(self, *args, **kwargs):
        church_instance = kwargs.pop('church_instance',None)
        super().__init__(*args, **kwargs)
        if church_instance:
            self.fields['service'].queryset = Service.objects.filter(church=church_instance)
        else:
            self.fields['service'].queryset = Service.objects.none()

    class Meta:
        model = ChurchRecord
        fields = (
            'service',
            'sermon_title',
            'text',
            'service_date',
            )