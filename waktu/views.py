from django.shortcuts import render
from django.shortcuts import render, redirect
from . import models
from datetime import datetime
import calendar
# from .decorators import role_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.forms import DateInput
import json
from django.db.models import F,Q,Sum,Value
import math
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
from django.urls import reverse

# Create your views here.
def loginview(request):
    if request.user.is_authenticated:
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'gudang':
            return redirect('base')
        elif group =='admin':
            return redirect('base3')
        elif group == 'owner' :
            return redirect('base4')
        else :
            return redirect('base2')
    else:
        return render(request,"base/login.html")
    
def performlogin(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        username_login = request.POST['username']
        password_login = request.POST['password']
        userobj = authenticate(request, username=username_login,password=password_login)
        if userobj is not None:
            login(request, userobj)
            messages.success(request,"Login success")
            if userobj.groups.filter(name='admin').exists() :
                return redirect("base3")
            elif userobj.groups.filter(name='owner').exists():
                return redirect('base4')
            elif userobj.groups.filter(name='gudang').exists() :
                return redirect("base")
            elif  userobj.groups.filter(name='produksi').exists() :
                return redirect('base2')
        else:
            messages.error(request,"Username atau Password salah !!!")
            return redirect("login")


@login_required(login_url="login")
def logoutview(request):
    logout(request)
    messages.info(request,"Berhasil Logout")
    return redirect('login')

@login_required(login_url="login")
def performlogout(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@role_required(["gudang"])  
def base(request) :
    alltransaksigudang = models.transaksigudang.objects.all().order_by('tanggal')
    detailtransaksi = []
    for i in alltransaksigudang :
        list_detailobj = []
        detailtransaksiobj = models.detailtransaksigudang.objects.filter(id_transaksigudang=i.id_transaksigudang).filter(keteranganacc = False)

        if not detailtransaksiobj.exists() :
            continue
        
        list_detailobj.append(i)
        list_detailobj.append(detailtransaksiobj)
        detailtransaksi.append(list_detailobj)
    print(detailtransaksi)

    allspp = models.suratjalanpembelian.objects.all().order_by('tanggal')
    detailspp = []
    for i in allspp :
        list_sppobj = []
        detailsppobj = models.detailsuratjalanpembelian.objects.filter(id_sjp = i.id_sjp).filter(keteranganacc = True)

        if not detailsppobj.exists() :
            continue
        list_sppobj.append(i)
        list_sppobj.append(detailsppobj)
        detailspp.append(list_sppobj)
  

    return render(request,'base/dashboard.html',{'transaksiobj':detailtransaksi,
     'sppobj' : detailspp})

@login_required(login_url="login")
@role_required(["produksi"])  
def base2(request) :
    alltransaksigudang2 = models.transaksigudang.objects.all().order_by('tanggal')
    detailtransaksi2 = []
    for i in alltransaksigudang2 :
        list_detailobj2 = []
        detailtransaksiobj2 = models.detailtransaksigudang.objects.filter(id_transaksigudang=i.id_transaksigudang).filter(keteranganacc = True)

        if not detailtransaksiobj2.exists() :
            continue
        
        list_detailobj2.append(i)
        list_detailobj2.append(detailtransaksiobj2)
        detailtransaksi2.append(list_detailobj2)
    print("detail2 :",detailtransaksi2)
  
    allspk = models.spk.objects.all().order_by('tanggal')
    detailspk = []
    for i in allspk :
        list_detailobj2 = []
        detailspkobj = models.detailspk.objects.filter(id_spk = i.id_spk).filter(status = False)

        if not detailspkobj.exists() :
            continue
        list_detailobj2.append(i)
        list_detailobj2.append(detailspkobj)
        detailspk.append(list_detailobj2)
    return render(request,'base/dashboard2.html',{'transaksiobj2':detailtransaksi2,'spkobj' :detailspk})

@login_required(login_url="login")
@role_required(["admin"])  
def base3(request) :
    allspp = models.suratjalanpembelian.objects.all().order_by('tanggal')
    detailspp = []
    for i in allspp :
        list_detailobj = []
        detailsppobj = models.detailsuratjalanpembelian.objects.filter(id_sjp = i.id_sjp).filter(keteranganacc = False)

        if not detailsppobj.exists() :
            continue
        list_detailobj.append(i)
        list_detailobj.append(detailsppobj)
        detailspp.append(list_detailobj)
    
    return render(request,'base/dashboard3.html',{'sppobj':detailspp})

@login_required(login_url="login")
@role_required(["owner"])  
def base4(request) :
    allspk = models.spk.objects.all().order_by('tanggal')
    detailspk = []
    for i in allspk :
        list_detailobj = []
        detailspkobj = models.detailspk.objects.filter(id_spk = i.id_spk).filter(status = True)

        if not detailspkobj.exists() :
            continue
        list_detailobj.append(i)
        list_detailobj.append(detailspkobj)
        detailspk.append(list_detailobj)
    
    return render(request,'base/dashboard4.html',{'spkobj':detailspk})

@login_required(login_url="login")
@role_required(["gudang"])  
def verif_transaksi(request,id) :
    transaksi = models.detailtransaksigudang.objects.get(id_detailtransaksigudang=id)

    transaksi.keteranganacc = True

    transaksi.save()
    messages.success(request, "Jangan lupa cek data gudang!")
    return redirect('base')

@login_required(login_url="login")
@role_required(["admin"])  
def verif_spp(request,id) :
    spp = models.detailsuratjalanpembelian.objects.get(id_detailsjp=id)

    spp.keteranganacc = True

    spp.save()
    messages.success(request, "SPP telah di ACC")
    return redirect('base3')

@login_required(login_url="login")
@role_required(["produksi"])  
def verif_spk(request,id) :
    spk = models.detailspk.objects.get(id_detailspk=id)

    spk.status = True

    spk.save()
    messages.success(request, "SPK telah di ACC")
    return redirect('base2')
   

'''CRUD ARTIKEL'''
@login_required(login_url="login")
@role_required(["owner",'admin'])  
def read_artikel(request) :
    artikelobj = models.artikel.objects.all()
    return render(request, 'artikel/read_artikel.html', {'artikelobj':artikelobj})

@login_required(login_url="login")
@role_required(["owner",'admin'])
def create_artikel(request) :
    if request.method == 'POST':
        kode_artikel = request.POST['kode_artikel']
        keterangan = request.POST['keterangan']

        filterartikel = models.artikel.objects.filter(kode_artikel=kode_artikel)
        if len(filterartikel)>0 :
            messages.error(request, 'Kode Artikel Sudah Ada')

        else :
            models.artikel(
                kode_artikel = kode_artikel,
                keterangan = keterangan
            ).save()
            messages.success(request, "Data berhasil dicreate!")
        return redirect('read_artikel')
    else :
        return render(request, 'artikel/create_artikel.html')

@login_required(login_url="login")
@role_required(["owner",'admin'])
def update_artikel(request,id) :
    getartikelobj = models.artikel.objects.get(id_artikel = id)
    print("get",getartikelobj)
    if request.method == "GET":
        return render(request, 'artikel/update_artikel.html', {
            'getartikelobj': getartikelobj,
        })
    else:
        kode_artikel = request.POST["kode_artikel"]
        if models.artikel.objects.filter(kode_artikel=kode_artikel).exclude(id_artikel = id).exists() :
            messages.error(request,"Nama artikel sudah ada!")
            return render(request, 'artikel/update_artikel.html', {
            'getartikelobj': getartikelobj,
            })
        
        getartikelobj.kode_artikel = request.POST["kode_artikel"]
        getartikelobj.keterangan = request.POST["keterangan"]
        
        getartikelobj.save()
        print("cek",getartikelobj)
        messages.success(request, "Artikel berhasil diperbarui!")
        return redirect('read_artikel')
   
@login_required(login_url="login")
@role_required(["owner"])
def delete_artikel(request,id) :
    getartikelobj = models.artikel.objects.get(id_artikel = id)
    getartikelobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_artikel')


'''CRUD BAHAN BAKU'''
@login_required(login_url="login")
@role_required(["owner",'admin'])
def read_bahanbaku(request) :
    bahanbaku = models.bahanbaku.objects.all()
    return render(request, 'bahanbaku/read_bahanbaku.html', {'bahanbaku':bahanbaku})

@login_required(login_url="login")
@role_required(["owner",'admin'])
def create_bahanbaku(request) :
    if request.method == 'POST':
        bahanbaku = request.POST['bahanbaku']
        satuan = request.POST['satuan']
        safetystock = request.POST['safetystock']
        filterbahanbaku = models.bahanbaku.objects.filter(nama_bahanbaku=bahanbaku)
        if len(filterbahanbaku)>0 :
            messages.error(request, 'Nama Bahan Baku Sudah Ada')

        else :
            models.bahanbaku(
                nama_bahanbaku = bahanbaku,
                satuan = satuan,
                safety_stock = safetystock
            ).save()
            messages.success(request, "Data berhasil dibuat!")
        return redirect('read_bahanbaku')
    else :
        return render(request, 'bahanbaku/create_bahanbaku.html')

@login_required(login_url="login")
@role_required(["owner",'admin',])
def update_bahanbaku(request,id) :
    getbahanbakuobj = models.bahanbaku.objects.get(id_bahanbaku = id)
    
    if request.method == "GET":
        return render(request, 'bahanbaku/update_bahanbaku.html', {
            'getbahanbakuobj': getbahanbakuobj,
            'id' : id
        })
    else:
        nama_bahanbaku = request.POST["nama_bahanbaku"]
        if models.bahanbaku.objects.filter(nama_bahanbaku=nama_bahanbaku).exclude(id_bahanbaku = id).exists() :
            messages.error(request,"Nama bahanbaku sudah ada!")
            return render(request, 'bahanbaku/update_bahanbaku.html', {
            'getbahanbakuobj': getbahanbakuobj,
            })
        
        getbahanbakuobj.nama_bahanbaku = request.POST["nama_bahanbaku"]
        getbahanbakuobj.satuan = request.POST["satuan"]
        getbahanbakuobj.safety_stock = request.POST["safety_stock"]
        
        getbahanbakuobj.save()
        messages.success(request, "Artikel berhasil diperbarui!")
        return redirect('read_bahanbaku')

@login_required(login_url="login")
@role_required(["owner"])
def delete_bahanbaku(request,id) :
    getbahanbakuobj = models.bahanbaku.objects.get(id_bahanbaku = id)
    getbahanbakuobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_bahanbaku')


'''CRUD SPK'''
@login_required(login_url="login")
@role_required(["owner",'admin','produksi'])
def read_spk(request) :
    spkobj = models.detailspk.objects.all().order_by('id_spk__tanggal')
    return render(request, 'spk/read_spk.html',{'detailspk':spkobj})

@login_required(login_url="login")
@role_required(["owner",'admin'])
def create_spk(request) :
    allartikel = models.artikel.objects.all()
    if request.method == 'POST' :
        no_spk = request.POST['no_spk']
        tanggal = request.POST['tanggal']
        kode_artikel  =request.POST.getlist('kode_artikel')
        jumlah = request.POST.getlist('jumlah')
        status = request.POST.getlist('status')

        savespk = models.spk(
            no_spk=no_spk,
            tanggal = tanggal
        )

        savespk.save()

        for kode_artikel,jumlah,status_spk in zip(kode_artikel,jumlah,status) :
            models.detailspk(
                id_spk = savespk,
                id_artikel = models.artikel.objects.get(id_artikel=kode_artikel),
                jumlah = jumlah,
                status = True if status_spk=='True' else False
            ).save()
        messages.success(request,"Data SPK Berhasil Ditambahkan!")
        return redirect("read_spk")

    else :
        return render(request,'spk/create_spk.html',{
            'allartikel' : allartikel
        })

@login_required(login_url="login")
@role_required(["owner",'admin','produksi'])
def update_spk(request,id) :
    getspkobj = models.detailspk.objects.get(id_detailspk=id)
    allartikel = models.artikel.objects.all()
    if request.method == 'POST':
        getspkobj.id_spk.no_spk= request.POST['no_spk']
        getspkobj.id_spk.tanggal= request.POST['tanggal']
        getspkobj.id_artikel  = models.artikel.objects.get( id_artikel =  request.POST['kode_artikel'])
        getspkobj.jumlah = request.POST['jumlah']
        statusspk = request.POST['status']
        getspkobj.status = True if statusspk=='True' else False
        getspkobj.id_spk.save()
        getspkobj.save()
        messages.success(request, "Data berhasil diperbarui!")
        return redirect('read_spk')

    else :
        tanggal = getspkobj.id_spk.tanggal.strftime('%Y-%m-%d')
        return render(request,"spk/update_spk.html",{
            'detailspk' :getspkobj,
            'tanggal' : tanggal,
            'allartikel' : allartikel
        })

@login_required(login_url="login")
@role_required(["owner"])  
def delete_spk(request,id) :
    getspkobj = models.detailspk.objects.get(id_detailspk=id)
    getspkobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_spk')

'''CRUD KONVERSI'''
@login_required(login_url="login")
@role_required(["owner",'admin','gudang','produksi'])
def read_konversi(request) :
    konversiobj = models.konversi.objects.all().order_by('versi')
    detailkonv = []

    for i in konversiobj :
        list_detailobj = []
        detailkonvobj = models.detailkonversi.objects.filter(id_konversi=i.id_konversi)

        if not detailkonvobj.exists() :
            continue
        
        list_detailobj.append(i)
        list_detailobj.append(detailkonvobj)
        detailkonv.append(list_detailobj)
    print(detailkonv)

    return render(request,"konversi/read_konversi.html",{
        'konversiobj' : detailkonv
    })


# def read_konversi(request) :
#     konversiobj = models.detailkonversi.objects.all()
#     return render(request,"konversi/read_konversi.html",{
#         'konversiobj' : konversiobj
#     })

@login_required(login_url="login")
@role_required(["owner",'produksi'])
def create_konversi(request) :
    allartikel = models.artikel.objects.all()
    allbahanbaku = models.bahanbaku.objects.all()
    if request.method == 'POST':
        kode_artikel = request.POST['kode_artikel']
        versi = request.POST['versi']
        nama_bahanbaku = request.POST.getlist('nama_bahanbaku')
        kuantitas = request.POST.getlist('kuantitas')
        print("bahan baku",nama_bahanbaku)
        savekonversi = models.konversi(
            id_artikel = models.artikel.objects.get(id_artikel = kode_artikel),
            versi = versi
        )

        savekonversi.save()

        for nama_bahanbaku,kuantitas in zip(nama_bahanbaku,kuantitas) :
            models.detailkonversi(
                id_konversi = savekonversi,
                id_bahanbaku = models.bahanbaku.objects.get(id_bahanbaku=nama_bahanbaku),
                kuantitas = kuantitas
            ).save()

        return redirect('read_konversi')
    else :  
        return render(request,"konversi/create_konversi.html",{
            
            'allartikel' : allartikel,
            'allbahanbaku' : allbahanbaku
        })

@login_required(login_url="login")
@role_required(["owner",'produksi'])   
def update_konversi(request,id):
    getkonversiobj = models.detailkonversi.objects.get(id_detailkonversi=id)
    allbahanbaku = models.bahanbaku.objects.all()
    print("id:",id)
    if request.method == 'POST':
        print("nama bahan",request.POST['nama_bahanbaku'])
        getkonversiobj.id_bahanbaku = models.bahanbaku.objects.get(id_bahanbaku = request.POST['nama_bahanbaku'])
        getkonversiobj.kuantitas = request.POST['kuantitas']

        getkonversiobj.save()
        messages.success(request, "Data berhasil diperbarui!")
        return redirect('read_konversi')

    else :
        
        return render(request,"konversi/update_konversi.html",{
            'detailkonversi': getkonversiobj,
            'allbahanbaku' : allbahanbaku,
        })
@login_required(login_url="login")
@role_required(["owner"])
def delete_konversi(request,id) :
    getkonversiobj = models.detailkonversi.objects.get(id_detailkonversi=id)
    getkonversiobj.delete()
    
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_konversi')

# UD KONVERSI AJA
@login_required(login_url="login")
@role_required(["owner",'produksi'])
def update_konv(request, id):
    konversiobj = models.konversi.objects.get( id_konversi=id)
    allartikel = models.artikel.objects.all()
    if request.method == 'POST':
        konversiobj.id_artikel =models.artikel.objects.get(id_artikel= request.POST['kode_artikel'])
        konversiobj.versi = request.POST['versi']
        konversiobj.save()

        # Update detailkonversi objects
        filterdetail = models.detailkonversi.objects.filter(id_konversi=konversiobj.id_konversi)
        for detail in filterdetail:
            detail.id_konversi = konversiobj  # This line is not really necessary as it is already set to konversiobj.id_konversi
            detail.save()

        return redirect('read_konversi')  # Redirect to the appropriate view after saving
    else :
        versi = konversiobj.versi.strftime('%Y-%m-%d')
        context = {
            'getkonversi': konversiobj,
            'allartikel': allartikel,
            'versi' :versi
        }
        return render(request, 'konversi/update_konv.html', context)
    
@login_required(login_url="login")
@role_required(["owner"])
def delete_konv(request,id) :
    getkonversiobj = models.konversi.objects.get(id_konversi=id)
    getkonversiobj.delete()
    
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_konversi')


'''CRUD DETAIL TRANSAKSI GUDANG'''
@login_required(login_url="login")
@role_required(["owner",'gudang','produksi'])
def read_transaksigudang(request) :
    alltransaksigudang = models.transaksigudang.objects.all().order_by('tanggal')

    detailtransaksi = []
    for i in alltransaksigudang :
        list_detailobj = []
        detailtransaksiobj = models.detailtransaksigudang.objects.filter(id_transaksigudang=i.id_transaksigudang)

        if not detailtransaksiobj.exists() :
            continue
        
        list_detailobj.append(i)
        list_detailobj.append(detailtransaksiobj)
        detailtransaksi.append(list_detailobj)
    print(detailtransaksi)

    return render(request,"transaksigudang/read_transaksigudang.html",{
        'detailtransaksiobj' : detailtransaksi
    })

@login_required(login_url="login")
@role_required(["owner",'produksi'])
def create_transaksigudang(request) :
    allbahanbaku = models.bahanbaku.objects.all()
    if request.method == 'POST':
        tanggal = request.POST['tanggal']
        nama_bahanbaku = request.POST.getlist('nama_bahanbaku')
        jumlah = request.POST.getlist('jumlah')
        keterangan = request.POST.getlist('keterangan')
        keteranganacc = request.POST.getlist('keterangan')

        savetransaksigudang = models.transaksigudang(
            tanggal = tanggal
        )

        savetransaksigudang.save()

        for nama_bahanbaku,jumlah,keterangan,keteranganacc in zip(nama_bahanbaku,jumlah,keterangan,keteranganacc) :
            models.detailtransaksigudang(
                id_transaksigudang = savetransaksigudang,
                id_bahanbaku = models.bahanbaku.objects.get(id_bahanbaku=nama_bahanbaku),
                jumlah = jumlah,
                keterangan = keterangan,
                keteranganacc = True if keteranganacc=='True' else False
            ).save()

        return redirect('read_transaksigudang')
    else :  
        return render(request,"transaksigudang/create_transaksigudang.html",{
            'allbahanbaku' : allbahanbaku
        })
    
@login_required(login_url="login")
@role_required(["owner",'gudang','produksi'])
def update_transaksigudang(request,id) :
    gettransaksigudangobj = models.detailtransaksigudang.objects.get(id_detailtransaksigudang=id)
    allbahanbaku = models.bahanbaku.objects.all()
    if request.method == 'POST':
        gettransaksigudangobj.id_bahanbaku = models.bahanbaku.objects.get(id_bahanbaku = request.POST['nama_bahanbaku'])
        gettransaksigudangobj.jumlah = request.POST['jumlah']
        gettransaksigudangobj.keterangan = request.POST['keterangan']
        
        keterangan_acc = request.POST.get('keteranganacc',False)
        if keterangan_acc=='True' :
            gettransaksigudangobj.keteranganacc = True
        else :
            gettransaksigudangobj.keteranganacc = False
        gettransaksigudangobj.save()
        messages.success(request, "Data berhasil diperbarui!")
        return redirect('read_transaksigudang')

    else :

        return render(request,"transaksigudang/update_transaksigudang.html",{
            'allbahanbaku' : allbahanbaku,
            'gettransaksigudangobj' :gettransaksigudangobj
        })

@login_required(login_url="login")
@role_required(["owner"])
def delete_transaksigudang(request,id) :
    gettransaksigudangobj = models.detailtransaksigudang.objects.get(id_detailtransaksigudang=id)

    gettransaksigudangobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_transaksigudang')

@login_required(login_url="login")
@role_required(["owner",'produksi'])
def update_transaksi(request,id) :
    gettransaksiobj = models.transaksigudang.objects.get(id_transaksigudang=id)

    if request.method == 'POST':
        gettransaksiobj.tanggal = request.POST['tanggal']
       
        gettransaksiobj.save()
        messages.success(request, "Data berhasil diperbarui!")
        return redirect('read_transaksigudang')

    else :
        tanggal = gettransaksiobj.tanggal.strftime('%Y-%m-%d')
        return render(request,"transaksigudang/update_transaksi.html",{
            'gettransaksiobj' : gettransaksiobj,
            'tanggal' : tanggal
        })
@login_required(login_url="login")
@role_required(["owner"])
def delete_transaksi(request,id) :
    gettransaksiobj = models.transaksigudang.objects.get(id_transaksigudang=id)

    gettransaksiobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_transaksigudang')


'''SPPB'''
@login_required(login_url="login")
@role_required(["owner",'admin','gudang'])
def read_detailsjp(request) :
    allsjp = models.suratjalanpembelian.objects.all().order_by('tanggal')

    detailsjp = []
    for i in allsjp :
        list_detailobj = []
        detailsuratjalanpembelianobj = models.detailsuratjalanpembelian.objects.filter(id_sjp=i.id_sjp)

        if not detailsuratjalanpembelianobj.exists() :
            continue
        
        list_detailobj.append(i)
        list_detailobj.append(detailsuratjalanpembelianobj)
        detailsjp.append(list_detailobj)


    return render(request,"sjp/read_detailsjp.html",{
        'detailsjp' : detailsjp
    })

@login_required(login_url="login")
@role_required(["owner",'gudang'])
def create_detailsjp(request) :
    allbahanbaku = models.bahanbaku.objects.all()
    if request.method == 'POST':
        tanggal = request.POST['tanggal']
        nama_bahanbaku = request.POST.getlist('nama_bahanbaku')
        jumlah = request.POST.getlist('jumlah')
        keterangan = request.POST.getlist('keterangan')
        keteranganacc = request.POST.getlist('keteranganacc')


        savesuratjalanpembelian = models.suratjalanpembelian(
            tanggal = tanggal
        )

        savesuratjalanpembelian.save()

        for nama_bahanbaku,jumlah,keterangan,keteranganacc in zip(nama_bahanbaku,jumlah,keterangan,keteranganacc) :
            models.detailsuratjalanpembelian(
                id_sjp = savesuratjalanpembelian,
                id_bahanbaku = models.bahanbaku.objects.get(id_bahanbaku=nama_bahanbaku),
                jumlah = jumlah,
                keterangan = keterangan,
                keteranganacc = True if keteranganacc== 'True' else False
            ).save()

        return redirect('read_detailsjp')
    else :  
        return render(request,"sjp/create_detailsjp.html",{
            'allbahanbaku' : allbahanbaku
        })
@login_required(login_url="login")
@role_required(["owner",'admin','gudang'])
def update_detailsjp(request,id) :
    getsuratjalanpembelianobj = models.detailsuratjalanpembelian.objects.get(id_detailsjp=id)
    allbahanbaku = models.bahanbaku.objects.all()
    if request.method == 'POST':
        getsuratjalanpembelianobj.id_bahanbaku = models.bahanbaku.objects.get(id_bahanbaku = request.POST['nama_bahanbaku'])
        getsuratjalanpembelianobj.jumlah = request.POST['jumlah']
        getsuratjalanpembelianobj.keterangan = request.POST['keterangan']
        keterangan_acc = request.POST.get('keteranganacc',False)
        if keterangan_acc=='True' :
            getsuratjalanpembelianobj.keteranganacc = True
        else :
            getsuratjalanpembelianobj.keteranganacc = False
        getsuratjalanpembelianobj.save()
        messages.success(request, "Data berhasil diperbarui!")
        return redirect('read_detailsjp')

    else :

        return render(request,"sjp/update_detailsjp.html",{
            'allbahanbaku' : allbahanbaku,
            'getsuratjalanpembelianobj' :getsuratjalanpembelianobj
        })
    
@login_required(login_url="login")
@role_required(["owner",'gudang'])
def delete_detailsjp(request,id) :
    getsuratjalanpembelianobj = models.detailsuratjalanpembelian.objects.get(id_detailsjp=id)

    getsuratjalanpembelianobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_detailsjp')

@login_required(login_url="login")
@role_required(["owner",'gudang'])
def update_sjp(request,id) :
    getsjpobj = models.suratjalanpembelian.objects.get(id_sjp=id)

    if request.method == 'POST':
        getsjpobj.tanggal = request.POST['tanggal']
       
        getsjpobj.save()
        messages.success(request, "Data berhasil diperbarui!")
        return redirect('read_detailsjp')

    else :
        tanggal = getsjpobj.tanggal.strftime('%Y-%m-%d')
        return render(request,"sjp/update_sjp.html",{
            'getsjpobj' : getsjpobj,
            'tanggal' : tanggal
        })
@login_required(login_url="login")
@role_required(["owner"])
def delete_sjp(request,id) :
    getsjpobj = models.suratjalanpembelian.objects.get(id_sjp=id)

    getsjpobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_detailsjp')

@login_required(login_url="login")
@role_required(["owner",'admin','gudang'])
def rekap_gudang(request) :
    tglmulai = request.GET.get('mulai')
    tglakhir = request.GET.get('akhir')

    print('mulai',tglmulai)
    sjp_dict = {}
    transaksigudang_dict = {}
    total_stok = {}
    
    if tglmulai and tglakhir:
        allbahanbaku = models.bahanbaku.objects.all()
        for i in allbahanbaku:
            bahanbaku = i.nama_bahanbaku
            minimal = i.safety_stock
            detailsjpobj = models.detailsuratjalanpembelian.objects.filter(
                id_bahanbaku__nama_bahanbaku=bahanbaku,
                id_sjp__tanggal__range=(tglmulai, tglakhir),keteranganacc = True
            ).values('id_bahanbaku__nama_bahanbaku').annotate(jumlah=Sum('jumlah')).order_by('id_sjp__tanggal')

            detailtransaksiobj = models.detailtransaksigudang.objects.filter(
                id_bahanbaku__nama_bahanbaku=bahanbaku,
                id_transaksigudang__tanggal__range=(tglmulai, tglakhir),keteranganacc = True
            ).values('id_bahanbaku__nama_bahanbaku').annotate(jumlah=Sum('jumlah')).order_by('id_transaksigudang__tanggal')
            
            if not detailsjpobj.exists() :
           
                continue
            
            for item in detailsjpobj:
                if item['id_bahanbaku__nama_bahanbaku'] in sjp_dict:
                    sjp_dict[item['id_bahanbaku__nama_bahanbaku']] += item['jumlah']
                else:
                    sjp_dict[item['id_bahanbaku__nama_bahanbaku']] = (item['jumlah'],minimal)


            for item2 in detailtransaksiobj:
                if item2['id_bahanbaku__nama_bahanbaku'] in transaksigudang_dict:
                    transaksigudang_dict[item2['id_bahanbaku__nama_bahanbaku']] += item2['jumlah']
                else:
                    transaksigudang_dict[item2['id_bahanbaku__nama_bahanbaku']] = item2['jumlah']

        for key in sjp_dict:
            jumlah_masuk = sjp_dict[key][0]
            jumlah_keluar = transaksigudang_dict.get(key, 0)
            
            print("jumlah masuk",jumlah_masuk)
            print("jumlah keluar",jumlah_keluar)

            total = jumlah_masuk - jumlah_keluar
            total_stok[key] = (total,sjp_dict[key][1])
        

        print(sjp_dict)
        print(transaksigudang_dict)
        print(total_stok)



        
    else :
        allbahanbaku = models.bahanbaku.objects.all()
        for i in allbahanbaku:
            bahanbaku = i.nama_bahanbaku
            minimal = i.safety_stock
            detailsjpobj = models.detailsuratjalanpembelian.objects.filter(
                id_bahanbaku__nama_bahanbaku=bahanbaku,
                keteranganacc = True
            ).values('id_bahanbaku__nama_bahanbaku').annotate(jumlah=Sum('jumlah')).order_by('id_sjp__tanggal')

            detailtransaksiobj = models.detailtransaksigudang.objects.filter(
                id_bahanbaku__nama_bahanbaku=bahanbaku,keteranganacc = True
            ).values('id_bahanbaku__nama_bahanbaku').annotate(jumlah=Sum('jumlah')).order_by('id_transaksigudang__tanggal')
            
            if not detailsjpobj.exists() :
                continue
            
            for item in detailsjpobj:
                if item['id_bahanbaku__nama_bahanbaku'] in sjp_dict:
                    sjp_dict[item['id_bahanbaku__nama_bahanbaku']] += item['jumlah']
                else:
                    sjp_dict[item['id_bahanbaku__nama_bahanbaku']] = (item['jumlah'],minimal)


            for item2 in detailtransaksiobj:
                if item2['id_bahanbaku__nama_bahanbaku'] in transaksigudang_dict:
                    transaksigudang_dict[item2['id_bahanbaku__nama_bahanbaku']] += item2['jumlah']
                else:
                    transaksigudang_dict[item2['id_bahanbaku__nama_bahanbaku']] = item2['jumlah']

        for key in sjp_dict:
            jumlah_masuk = sjp_dict[key][0]
            jumlah_keluar = transaksigudang_dict.get(key, 0)
            
            print("jumlah masuk",jumlah_masuk)
            print("jumlah keluar",jumlah_keluar)

            total = jumlah_masuk - jumlah_keluar
            total_stok[key] = (total,sjp_dict[key][1])
        

        print(sjp_dict)
        print(transaksigudang_dict)
        print(total_stok)

    return render(request,'rekap/rekap_gudang.html',
                      {
                          'total_stok' : total_stok,
                          'mulai' : tglmulai,
                          'akhir' : tglakhir,
                      }
                      )

@login_required(login_url="login")
@role_required(["owner",'admin','gudang','produksi'])
def rekap_konv(request):
    allspk = models.spk.objects.all().order_by('tanggal')
    if len(request.GET) == 0:
        return render(request, 'rekap/rekap_konversi.html', {
            'allspk': allspk
        })
    else:
        spk = request.GET['spk']
        detailspkobj = models.detailspk.objects.filter(id_spk=spk, status=False)
        
        if not detailspkobj.exists() :
            messages.error(request,"Konversi untuk data SPK ini tidak ditemukan!")
        konvlist = []

        for i in detailspkobj:
            dummy = []
            artikel = i.id_artikel
            jumlah = i.jumlah
            konversiobj = models.konversi.objects.filter(id_artikel=artikel).order_by('versi')
            dummy.append(artikel)
            dummy.append(jumlah)

            if not konversiobj.exists():
                messages.error(request, "Data Konversi Tidak ditemukan")
                return redirect('rekap_konv')

            dummylast = []
            for a in konversiobj:
                dummykonv = []
                detailkonvobj = models.detailkonversi.objects.filter(id_konversi=a)

                if not detailkonvobj.exists():
                    continue
                
                dummykonv.append(a)  # Menambahkan objek konversi
                dummytotal = []
                for detail in detailkonvobj:
                    kuantitas = detail.kuantitas * jumlah  # Menghitung kuantitas total
                    dummytotal.append(kuantitas)
                
                dummykonv.append(list(detailkonvobj))  # Menambahkan detail konversi
                dummykonv.append(dummytotal)  # Menambahkan kuantitas total

                dummylast.append(dummykonv)

            dummy.append(dummylast)
            konvlist.append(dummy)

        print('konv', konvlist)
        return render(request, 'rekap/rekap_konversi.html', {
            'datakonv': konvlist,
            'spk' :spk,
            'allspk': allspk
        })
