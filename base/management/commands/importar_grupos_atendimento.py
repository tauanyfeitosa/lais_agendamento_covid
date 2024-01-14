import xml.etree.ElementTree as ET

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from base.models import GrupoAtendimento


class Command(BaseCommand):
    help = 'Importa grupos de atendimento do XML'

    def handle(self, *args, **kwargs):
        try:
            response = requests.get('https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml')
            xml_data = response.content

            root = ET.fromstring(xml_data)

            for grupo in root.findall('grupoatendimento'):
                nome = grupo.find('nome').text
                codigo_si_pni = grupo.find('codigo_si_pni').text

                with transaction.atomic():
                    GrupoAtendimento.objects.update_or_create(
                        nome=nome,
                        defaults={
                            'codigo_si_pni': codigo_si_pni or '',
                        }
                    )

            self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar grupos de atendimento: {e}'))
