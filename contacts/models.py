from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length = 254)
    birthday = models.DateField('nascimento', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
