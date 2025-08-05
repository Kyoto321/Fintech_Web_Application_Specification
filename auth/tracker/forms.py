from django import forms
from tracker.models import Transaction, Category


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be a positive number")
        return amount

    # def acc_digits(self):
    #     account_number = self.cleaned_data['account_number']
    #     if account_number < 10 or account_number > 10:
    #         raise forms.ValidationError("Account number must be 10 digits")
    #     return account_number

    class Meta:
        model = Transaction
        fields = (
            'type',
            # 'bank',
            # 'account_number',
            'amount',
            'date',
            'category',       
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }