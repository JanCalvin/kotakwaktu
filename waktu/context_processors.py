def is_owner(request) :
    return {'is_owner': request.user.groups.filter(name='owner').exists()}
def is_admin(request) :
    return {'is_admin': request.user.groups.filter(name='admin').exists()}
def is_produksi(request) :
    return {'is_produksi': request.user.groups.filter(name='produksi').exists()}
def is_gudang(request) :
    return {'is_gudang': request.user.groups.filter(name='gudang').exists()}