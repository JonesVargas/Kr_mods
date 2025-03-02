from .models import HomePage, RedeSocial

def get_logo(request):
    homepage = HomePage.objects.first()
    return {'homepage': homepage}

def redes_sociais(request):
    return {'redes_sociais': RedeSocial.objects.all()}
