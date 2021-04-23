from django.db import models
import uuid
from django.utils import timezone
from django.db.models import Sum



    
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
class SoftDeletableQS(models.QuerySet):
   """A queryset that allows soft-delete on its objects""" 

   def delete(self, **kwargs):
       self.update(deleted_ts=timezone.now(), **kwargs)

   def hard_delete(self, **kwargs):
       super().delete(**kwargs)

class SoftDeletableManager(models.Manager):
   """Manager that filters out soft-deleted objects"""
   def get_queryset(self):
       return SoftDeletableQS(
           model=self.model, using=self._db, hints=self._hints
       ).filter(
           deleted_ts__isnull=True
       )

class SoftDeletableModel(models.Model):
   """An abstract parent class for soft-deletable models"""
   objects = SoftDeletableManager()
   archive_objects = models.Manager() 

   deleted_ts=models.DateTimeField(blank=True,null=True, editable=False)

   class Meta:
       abstract=True
   
   def delete(self):
       """Softly delete the object"""
       self.deleted_ts = timezone.now()
       self.save()

       

   
   def hard_delete(self):
       """Remove the object permanently from the database"""
       super().delete()

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, null=True, unique=False, editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True

class Brand(BaseModel, SoftDeletableModel):
    name=models.CharField(max_length=20, blank=False, null=True)

    def __str__(self):
        return str(self.name)


class ArchivedBrandManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedBrandManager, self).get_queryset().filter(deleted_ts__isnull=False)

class ArchivedBrand(Brand):
    """Archive transactions - hard-deletable"""
    objects = ArchivedBrandManager()
    #objects = models.Manager()

    class Meta:
        proxy=True

    def delete(self):
        """Permanently delete the entry"""
        super().hard_delete()

class Model(BaseModel, SoftDeletableModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    name=models.CharField(max_length=20, blank=False, null=True)

    def __str__(self):
        return "{} | {}".format(self.brand, self.name)

class ArchivedModelManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedModelManager, self).get_queryset().filter(deleted_ts__isnull=False)

class ArchivedModel(Model):
    """Archive transactions - hard-deletable"""
    objects = ArchivedModelManager()
    #objects = models.Manager()

    class Meta:
        proxy=True

    def delete(self):
        """Permanently delete the entry"""
        super().hard_delete()



class Color(BaseModel, SoftDeletableModel):
    name=models.CharField(max_length=20, blank=False, null=True)

    def __str__(self):
        return str(self.name)

class ArchivedColorManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedColorManager, self).get_queryset().filter(deleted_ts__isnull=False)

class ArchivedColor(Color):
    """Archive transactions - hard-deletable"""
    objects = ArchivedColorManager()
    #objects = models.Manager()

    class Meta:
        proxy=True

    def delete(self):
        """Permanently delete the entry"""
        super().hard_delete()

class Size(BaseModel, SoftDeletableModel):
    name=models.CharField(max_length=20, blank=False, null=True)

    def __str__(self):
        return str(self.name)

class ArchivedSizeManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedSizeManager, self).get_queryset().filter(deleted_ts__isnull=False)

class ArchivedSize(Size):
    """Archive transactions - hard-deletable"""
    objects = ArchivedSizeManager()
    #objects = models.Manager()

    class Meta:
        proxy=True

    def delete(self):
        """Permanently delete the entry"""
        super().hard_delete()


class Product(BaseModel, SoftDeletableModel):
    name = models.CharField(max_length=60, blank=True, null=True, help_text='title of the product')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, blank=True, null=True, help_text='if model is unfamiliar, search item ean at upcitemdb.com')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    ean = models.CharField(max_length=500, blank=False, null=True)
    ean2 = models.TextField(blank=False, null=True)
    note = models.CharField(max_length=120, blank=True, null=True, help_text='type your notes here about this item')

    def __str__(self):
        return "{} | {} | {}".format(str(self.model),str(self.size),str(self.color))

    @property
    def current_stock(self):
        total = self.logs.all().aggregate(Sum('quantity'))['quantity__sum']
        return total

class ArchivedProductManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedProductManager, self).get_queryset().filter(deleted_ts__isnull=False)

class ArchivedProduct(Product):
    """Archive transactions - hard-deletable"""
    objects = ArchivedProductManager()
    #objects = models.Manager()

    class Meta:
        proxy=True

    def delete(self):
        """Permanently delete the entry"""
        super().hard_delete()

class InventoryLog(BaseModel, SoftDeletableModel):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=True, related_name='logs')
    quantity = models.IntegerField(default=0, blank=False, null=True)

    def __str__(self):
        return str(self.product)

    @property
    def current_stock(self):
        total = InventoryLog.objects.filter(product=self.product).aggregate(Sum('quantity'))['quantity__sum']
        return total


class ArchivedInventoryLogManager(models.Manager):
    def get_queryset(self):
        return super(ArchivedInventoryLogManager, self).get_queryset().filter(deleted_ts__isnull=False)

class ArchivedInventoryLog(InventoryLog):
    """Archive transactions - hard-deletable"""
    objects = ArchivedInventoryLogManager()
    #objects = models.Manager()

    class Meta:
        proxy=True

    def delete(self):
        """Permanently delete the entry"""
        super().hard_delete()
