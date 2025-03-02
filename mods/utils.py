import boto3
from django.core.files.storage import default_storage
from mods.models import SectionContent, RedeSocial, Mod, HomePage, ApresentacaoImagem, Noticia
from django.core.wsgi import get_wsgi_application
import os

# Configurar Django manualmente (caso rode fora do manage.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modsite.settings')
get_wsgi_application()

# S3 Config
s3_client = boto3.client('s3')
bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

def migrate_image(instance, field_name, new_path_template):
    image_field = getattr(instance, field_name)

    if not image_field:
        return

    old_path = image_field.name
    if not old_path:
        return

    filename = old_path.split('/')[-1]
    new_path = new_path_template.format(id=instance.id, filename=filename)

    with default_storage.open(old_path, 'rb') as img_file:
        s3_client.upload_fileobj(img_file, bucket_name, new_path)

    setattr(instance, field_name, new_path)
    instance.save()

def run():
    print("Migrando imagens...")

    for conteudo in SectionContent.objects.all():
        migrate_image(conteudo, 'imagem', 'conteudo_{id}_{filename}')

    for rede in RedeSocial.objects.all():
        migrate_image(rede, 'icone', 'icone_{nome}_{filename}'.format(nome=rede.nome))

    for mod in Mod.objects.all():
        migrate_image(mod, 'image', 'mod_{id}_{filename}')
        migrate_image(mod, 'file', 'mod_file_{id}_{filename}')

    for homepage in HomePage.objects.all():
        migrate_image(homepage, 'logo', 'logo_{filename}')

    for apresentacao in ApresentacaoImagem.objects.all():
        migrate_image(apresentacao, 'imagem', 'apresentacao_{id}_{filename}')

    for noticia in Noticia.objects.all():
        migrate_image(noticia, 'imagem', 'noticia_{id}_{filename}')

    print("Migração de imagens concluída!")

if __name__ == '__main__':
    run()
