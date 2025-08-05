from django.db import models 


class TransactionQuerySet(models.QuerySet):
    def get_transfers(self):
        return self.filter(type='transfer')
    
    def get_payments(self):
        return self.filter(type='payment')
    
    def get_total_transfers(self):
        return self.get_transfers().aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def get_total_payments(self):
        return self.get_payments().aggregate(
            total=models.Sum('amount')
        )['total'] or 0
