from django import forms
from django.forms import formset_factory
from .models import Student, SchoolYear, Enrollment, STATUS_CHOICES


def _apply_bootstrap_controls(form):
    """Add Bootstrap classes to widgets for better mobile usability."""
    for name, field in form.fields.items():
        widget = field.widget
        # Skip HiddenInput
        if isinstance(widget, forms.HiddenInput):
            continue
        # Selects
        if isinstance(widget, (forms.Select, forms.SelectMultiple)):
            widget.attrs["class"] = (widget.attrs.get("class", "") + " form-select").strip()
        # Checkboxes & radios
        elif isinstance(widget, (forms.CheckboxInput,)):
            widget.attrs["class"] = (widget.attrs.get("class", "") + " form-check-input").strip()
        elif isinstance(widget, forms.RadioSelect):
            # Radio buttons styled via btn-check in template; avoid form-control
            widget.attrs["class"] = (widget.attrs.get("class", "") + " btn-check").strip()
        # Everything else (text, number, date, textarea, etc.)
        else:
            widget.attrs["class"] = (widget.attrs.get("class", "") + " form-control").strip()


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'lrn', 'last_name', 'first_name', 'middle_name', 'sex', 'birthdate'
        ]
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'birthdate': 'Optional for now',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Better mobile keyboard for numeric LRN
        if 'lrn' in self.fields:
            attrs = self.fields['lrn'].widget.attrs
            attrs.update({'inputmode': 'numeric', 'autocomplete': 'off', 'pattern': '[0-9]*'})
        _apply_bootstrap_controls(self)


class SchoolYearForm(forms.ModelForm):
    class Meta:
        model = SchoolYear
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap_controls(self)


class SingleAttendanceForm(forms.Form):
    enrollment_id = forms.IntegerField(widget=forms.HiddenInput())
    student_name = forms.CharField(disabled=True, required=False)
    status_am = forms.ChoiceField(label='AM', choices=STATUS_CHOICES, widget=forms.RadioSelect)
    status_pm = forms.ChoiceField(label='PM', choices=STATUS_CHOICES, widget=forms.RadioSelect)
    remarks = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'rows': 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap_controls(self)


AttendanceFormSet = formset_factory(SingleAttendanceForm, extra=0)
