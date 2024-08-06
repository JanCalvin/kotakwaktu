from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginview,name='login'),
    path('performlogin',views.performlogin,name="performlogin"),
    path('performlogout',views.performlogout,name="performlogout"),
    path('base', views.base, name='base'),
    path('base2', views.base2, name='base2'),
    path('base3', views.base3, name='base3'),
    path('base4', views.base4, name='base4'),
    path('verif_transaksi/<str:id>', views.verif_transaksi, name='verif_transaksi'),
    path('verif_spp/<str:id>', views.verif_spp, name='verif_spp'),
    path('verif_spk/<str:id>', views.verif_spk, name='verif_spk'),

    # CRUD ARTIKEL
    path('create_artikel', views.create_artikel,name='create_artikel'),
    path('read_artikel', views.read_artikel,name='read_artikel'),
    path('update_artikel/<str:id>', views.update_artikel,name='update_artikel'),
    path('delete_artikel/<str:id>', views.delete_artikel,name='delete_artikel'),

    # CRUD BAHAN BAKU
    path('create_bahanbaku', views.create_bahanbaku,name='create_bahanbaku'),
    path('read_bahanbaku', views.read_bahanbaku,name='read_bahanbaku'),
    path('update_bahanbaku/<str:id>', views.update_bahanbaku,name='update_bahanbaku'),
    path('delete_bahanbaku/<str:id>', views.delete_bahanbaku,name='delete_bahanbaku'),

    # CRUD SPK
    path('create_spk', views.create_spk,name='create_spk'),
    path('read_spk', views.read_spk,name='read_spk'),
    path('update_spk/<str:id>', views.update_spk,name='update_spk'),
    path('delete_spk/<str:id>', views.delete_spk,name='delete_spk'),

    # CRUD KONVERSI
    path('create_konversi', views.create_konversi,name='create_konversi'),
    path('read_konversi', views.read_konversi,name='read_konversi'),
    path('update_konversi/<str:id>', views.update_konversi,name='update_konversi'),
    path('delete_konversi/<str:id>', views.delete_konversi,name='delete_konversi'),
    path('update_konv/<str:id>', views.update_konv,name='update_konv'),
    path('delete_konv/<str:id>', views.delete_konv,name='delete_konv'),

    # CRUD TRANSAKSI GUDANG
    path('create_transaksigudang', views.create_transaksigudang,name='create_transaksigudang'),
    path('read_transaksigudang', views.read_transaksigudang,name='read_transaksigudang'),
    path('update_transaksigudang/<str:id>', views.update_transaksigudang,name='update_transaksigudang'),
    path('delete_transaksigudang/<str:id>', views.delete_transaksigudang,name='delete_transaksigudang'),
    path('update_transaksi/<str:id>', views.update_transaksi,name='update_transaksi'),
    path('delete_transaksi/<str:id>', views.delete_transaksi,name='delete_transaksi'),

    # CRUD SJP
    path('create_detailsjp', views.create_detailsjp,name='create_detailsjp'),
    path('read_detailsjp', views.read_detailsjp,name='read_detailsjp'),
    path('update_detailsjp/<str:id>', views.update_detailsjp,name='update_detailsjp'),
    path('delete_detailsjp/<str:id>', views.delete_detailsjp,name='delete_detailsjp'),
    path('update_sjp/<str:id>', views.update_sjp,name='update_sjp'),
    path('delete_sjp/<str:id>', views.delete_sjp,name='delete_sjp'),

    path('rekap_gudang', views.rekap_gudang,name='rekap_gudang'),
    path('rekap_konv', views.rekap_konv,name='rekap_konv'),
]