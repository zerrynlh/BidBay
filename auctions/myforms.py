"""Forms to import"""
from django import forms

#List of item categories
categories = [('', 'Select a category'),
              ('1', 'Bedroom') ,
              ('2', 'Living Room'),
              ('3', 'Kitchen'),
              ('4', 'Office'),
              ('5', 'Dining Room'),
              ('6', 'Entertainment'),
              ('7', 'Outdoor'),
              ('8', 'Bathroom'),
              ('9', 'Sports'),
              ('10', 'Auto'),
              ('11', 'Electronics'),
              ('12', 'Clothing'),
              ('13', 'Beauty'),
              ('14', 'Other')]

#List of item categories
filters = [('0', 'All Categories'),
              ('1', 'Bedroom') ,
              ('2', 'Living Room'),
              ('3', 'Kitchen'),
              ('4', 'Office'),
              ('5', 'Dining Room'),
              ('6', 'Entertainment'),
              ('7', 'Outdoor'),
              ('8', 'Bathroom'),
              ('9', 'Sports'),
              ('10', 'Auto'),
              ('11', 'Electronics'),
              ('12', 'Clothing'),
              ('13', 'Beauty'),
              ('14', 'Other')]

class ListingForm(forms.Form):
    """Form for user listings"""
    thetitle = forms.CharField (
        label="Title",
        widget=forms.TextInput (
            attrs={'placeholder': 'Enter a title', 'class' : 'form-control'}
            )
        )
    thedescription = forms.CharField (
        label="Description",
        widget=forms.Textarea (
            attrs={'placeholder': 'Enter text here...', 'class' : 'form-control'}
            )
        )
    theprice = forms.FloatField (
        label="Starting Bid",
        widget=forms.NumberInput (
            attrs={'placeholder': 'Enter a price', 'class' : 'form-control', 'min' : '0.00' }
            )
        )
    thepicture = forms.URLField(
        label="Image URL",
        widget=forms.URLInput(
            attrs={'placeholder': 'Enter a URL ', 'class' : 'form-control'}
            )
        )
    thecategory = forms.ChoiceField(
        label="Category",
        choices = categories, widget=forms.Select(
            attrs={'class' : 'form-control'}
            )
        )

class BidForm(forms.Form):
    """Bidding form"""
    thebid = forms.FloatField (
        label="Place Bid",
        widget=forms.NumberInput (
            attrs={
                'placeholder' : 'Ex: 5.00',
                'class' : 'form-control',
                'min' : '0.00',
                'name' : 'place_bid'
                }
            )
        )

class CommentForm(forms.Form):
    """Comment form"""
    thecomment = forms.CharField (
        widget=forms.Textarea (
            attrs={
                'placeholder' : 'Type your comment...',
                   'class' : 'form-control',
                   'max_length' : '200',
                   'rows' : '5',
                   'name' : 'add_comment'
                }
            )
        )

class FilterForm(forms.Form):
    """Filter listings"""
    thefilter = forms.ChoiceField (
        choices = filters,
        widget=forms.Select (
            attrs={
                'class' : 'form-control',
                'style' : 'width: 30vh;'
                }
            )
        )
