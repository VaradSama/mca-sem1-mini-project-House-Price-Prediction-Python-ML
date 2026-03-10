from django import forms

class HouseForm(forms.Form):
    location = forms.ChoiceField(
        choices=[('Urban', 'Urban'), ('Rural', 'Rural')],
        initial='Urban',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    total_sqft = forms.FloatField(
        label='Total Square Feet',
        initial=1000.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bhk = forms.IntegerField(
        label='Bedrooms (BHK)',
        initial=3,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bath = forms.IntegerField(
        label='Bathrooms',
        initial=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    year_built = forms.IntegerField(
        initial=2000,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    has_garage = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        initial='no',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
