from django.db import models

# Create your models here.

class artikel(models.Model) :
    id_artikel = models.AutoField(primary_key=True)
    kode_artikel = models.CharField( max_length=100)
    keterangan =models.TextField(blank=True, null=True)

    def __str__(self) :
        return str(self.kode_artikel)

class bahanbaku(models.Model) :
    id_bahanbaku= models.AutoField(primary_key=True)
    nama_bahanbaku = models.CharField(max_length=100)
    satuan =models.CharField(max_length=100)
    safety_stock = models.PositiveIntegerField()

    def __str__(self) :
        return str(self.nama_bahanbaku)

class spk(models.Model) :
    id_spk = models.AutoField(primary_key=True)
    no_spk = models.CharField(max_length=100)
    tanggal = models.DateField()
    
    def __str__(self) :
        return str(self.no_spk)
    
class detailspk(models.Model) :
    id_detailspk = models.AutoField(primary_key=True)
    id_spk = models.ForeignKey(spk, on_delete=models.CASCADE)
    id_artikel = models.ForeignKey(artikel,on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    status = models.BooleanField(default=False,null=True)

    def __str__(self) :
        return str(self.id_detailspk)
    
class konversi(models.Model) :
    id_konversi = models.AutoField(primary_key=True)
    id_artikel = models.ForeignKey(artikel,on_delete=models.CASCADE)
    versi = models.DateField()
    
    def __str__(self) :
        return "{} - {}".format(self.id_artikel,self.versi)
    

class detailkonversi(models.Model) :
    id_detailkonversi = models.AutoField(primary_key=True)
    id_konversi = models.ForeignKey(konversi,on_delete=models.CASCADE)
    id_bahanbaku = models.ForeignKey(bahanbaku,on_delete=models.CASCADE)
    kuantitas = models.FloatField()

    def __str__(self) :
        return str(self.id_detailkonversi)

class transaksigudang(models.Model) : 
    id_transaksigudang = models.AutoField(primary_key=True)
    tanggal = models.DateField()
    def __str__(self) :
        return str(self.id_transaksigudang)

class detailtransaksigudang(models.Model) :
    id_detailtransaksigudang = models.AutoField(primary_key=True)
    id_transaksigudang = models.ForeignKey(transaksigudang,on_delete=models.CASCADE)
    id_bahanbaku = models.ForeignKey(bahanbaku,on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    keterangan = models.TextField(blank=True, null=True)
    keteranganacc = models.BooleanField(default=False,null=True)
    def __str__(self) :
        return str(self.id_detailtransaksigudang)

class suratjalanpembelian(models.Model) :
    id_sjp = models.AutoField(primary_key=True)
    tanggal = models.DateField()
    def __str__(self) :
        return str(self.id_sjp)
    
class detailsuratjalanpembelian(models.Model) :
    id_detailsjp = models.AutoField(primary_key=True)
    id_sjp = models.ForeignKey(suratjalanpembelian,on_delete=models.CASCADE)
    id_bahanbaku = models.ForeignKey(bahanbaku,on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    keterangan = models.TextField(blank=True, null=True)
    keteranganacc = models.BooleanField(default=False,null=True)
    def __str__(self) :
        return str(self.id_detailsjp)