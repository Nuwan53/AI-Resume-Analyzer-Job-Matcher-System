"""
Forms for Resume AI Analyzer
"""

from django import forms
from .models import ExtarctedData


class ExtractedDataForm(forms.ModelForm):
    """Form for editing extracted resume data."""
    
    class Meta:
        model = ExtarctedData
        fields = ['skills', 'experience', 'education']
        widgets = {
            'skills': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'e.g., Python, Django, JavaScript, React, SQL, Docker...',
                'rows': 5,
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; font-family: monospace; font-size: 0.95rem;'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'e.g., 3 years as Senior Developer at Tech Corp, 2 years as Junior Developer at StartUp...',
                'rows': 6,
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; font-family: monospace; font-size: 0.95rem;'
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'e.g., B.S. Computer Science from University of Tech, 2020...',
                'rows': 4,
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; font-family: monospace; font-size: 0.95rem;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add labels
        self.fields['skills'].label = 'Technical Skills'
        self.fields['skills'].help_text = 'Enter comma-separated skills or on separate lines'
        
        self.fields['experience'].label = 'Professional Experience'
        self.fields['experience'].help_text = 'Describe your work experience, roles, and achievements'
        
        self.fields['education'].label = 'Education & Certifications'
        self.fields['education'].help_text = 'List your degrees, certifications, and training'
