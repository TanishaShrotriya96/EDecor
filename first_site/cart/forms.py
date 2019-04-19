from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)] #it gives the option to select the number of items to add to the cart


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int) #number of items to buy
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput) # it is used to update the quantity number
