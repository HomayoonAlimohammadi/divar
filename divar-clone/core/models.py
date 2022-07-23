from django.db import models
from django.contrib.auth import get_user_model 


User = get_user_model()

class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Item(name: {self.name}, price: {self.price})'