from .models import HomePage

def get_logo(request):
    homepage = HomePage.objects.first()
    return {'homepage': homepage}

from .models import RedeSocial

def redes_sociais(request):
    return {'redes_sociais': RedeSocial.objects.all()}
