from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import MyFormModel, LessonPlan, Subject, Grade, Standard, Material, Resource


class MyForm(forms.ModelForm):
    """Legacy form - keeping for backward compatibility"""
    class Meta:
        model = MyFormModel
        fields = '__all__'


class LessonPlanForm(forms.ModelForm):
    """Comprehensive lesson plan creation form"""
    lesson_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = LessonPlan
        fields = [
            'title', 'description', 'subject', 'grade', 'lesson_date', 'duration',
            'learning_objectives', 'essential_question', 'materials_needed',
            'opening_activity', 'main_instruction', 'guided_practice',
            'independent_practice', 'closing_activity',
            'formative_assessment', 'summative_assessment', 'differentiation_strategies',
            'homework_assignment', 'extension_activities', 'standards', 'is_public'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lesson title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the lesson'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'learning_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What will students learn or be able to do?'}),
            'essential_question': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Key question driving the lesson (optional)'}),
            'materials_needed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List required materials and resources'}),
            'opening_activity': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How will the lesson begin?'}),
            'main_instruction': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Core teaching and learning activities'}),
            'guided_practice': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Structured practice with teacher support (optional)'}),
            'independent_practice': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Individual student work (optional)'}),
            'closing_activity': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'How will the lesson conclude?'}),
            'formative_assessment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'How will you check for understanding?'}),
            'summative_assessment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'How will learning be evaluated? (optional)'}),
            'differentiation_strategies': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Accommodations for different learners'}),
            'homework_assignment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any assigned homework (optional)'}),
            'extension_activities': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Activities for early finishers (optional)'}),
            'standards': forms.CheckboxSelectMultiple(),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lesson_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-light text-dark'}), # Added for contrast
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter standards based on selected subject and grade if available
        if 'subject' in self.data and 'grade' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                grade_id = int(self.data.get('grade'))
                self.fields['standards'].queryset = Standard.objects.filter(
                    subject_id=subject_id, grade_id=grade_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['standards'].queryset = Standard.objects.filter(
                subject=self.instance.subject, grade=self.instance.grade
            )
        else:
            self.fields['standards'].queryset = Standard.objects.none()


class MaterialForm(forms.ModelForm):
    """Form for creating teaching materials"""
    
    class Meta:
        model = Material
        fields = ['title', 'description', 'content', 'file', 'url', 'material_type', 
                 'subject', 'grade', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ResourceForm(forms.ModelForm):
    """Form for creating external resources"""
    
    class Meta:
        model = Resource
        fields = ['title', 'url', 'description', 'resource_type', 'subject', 'grade', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class LessonSearchForm(forms.Form):
    """Form for searching and filtering lessons"""
    query = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search lessons...'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="All Subjects",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all(),
        required=False,
        empty_label="All Grades",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    duration = forms.ChoiceField(
        choices=[('', 'Any Duration')] + LessonPlan.DURATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class UserProfileForm(UserChangeForm):
    password = None  # Remove password field
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Optionally remove help text or make fields not required if needed
        # For example, to make email not required:
        # self.fields['email'].required = False