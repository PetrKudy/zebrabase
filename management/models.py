from django.db import models

class Room(models.Model):
    number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.id)

class Rack(models.Model):
    row_max = models.IntegerField()
    column_max = models.IntegerField()
    name = models.CharField(max_length = 100)
    room_id = models.ForeignKey(Room,to_field='id', on_delete=models.CASCADE)

class Position(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()
    rack_id = models.ForeignKey(Rack, on_delete=models.CASCADE)


class Substock(models.Model):
    amount = models.IntegerField()
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)



class Stock(models.Model):
    birthdate = models.DateField()
    substock_id = models.ForeignKey(Substock,to_field='id',related_name ='stock', on_delete=models.CASCADE)


class Fishline(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock_id = models.ForeignKey(Stock,to_field='id',related_name = 'fishline', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
