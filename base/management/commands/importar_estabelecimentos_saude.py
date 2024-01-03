from django.core.management.base import BaseCommand
import requests
import xml.etree.ElementTree as ET

from django.db import transaction

from base.models import EstabelecimentoSaude


class Command(BaseCommand):
    help = 'Importa estabelecimentos de saúde do XML'

    def handle(self, *args, **kwargs):
        try:
            response = requests.get('https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml')
            xml_data = response.content

            root = ET.fromstring(xml_data)

            for estabelecimento in root.findall('estabelecimento'):
                nome_fantasia = estabelecimento.find('no_fantasia').text
                codigo_cnes = estabelecimento.find('co_cnes').text

                with transaction.atomic():
                    EstabelecimentoSaude.objects.update_or_create(
                        codigo_cnes=codigo_cnes,
                        defaults={
                            'nome': nome_fantasia
                        }
                    )

            self.stdout.write(self.style.SUCCESS('Importação de estabelecimentos de saúde concluída com sucesso!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar estabelecimentos de saúde: {e}'))
