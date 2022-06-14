from django.db import models


class Round(models.Model):
    word = models.CharField(max_length=5, null=False, blank=False)
    datetime = models.DateTimeField(null=False, blank=False)
    
    @classmethod
    def get_current_round(cls) -> 'Round':
        return cls.objects.latest('datetime')
    
    @classmethod
    def get_round_before(cls) -> 'Round':
        return cls.objects.filter(datetime__lt=Round.get_current_round().datetime).latest('datetime')

    def __str__(self):
        return f"{self.datetime} | {self.word}"


class Guess(models.Model):
    word = models.CharField(max_length=5, null=False, blank=False)
    round = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural = "Guesses"
    
    
    def __str__(self):
        return f"{self.round.datetime} | {self.ip_address} | {self.word}"


