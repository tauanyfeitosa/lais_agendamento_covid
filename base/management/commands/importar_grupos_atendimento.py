from django.core.management.base import BaseCommand
import requests
import xml.etree.ElementTree as ET

from django.db import transaction
from django.utils.dateparse import parse_datetime
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
                visivel = grupo.find('visivel').text == 'true'
                fase = grupo.find('fase').text
                codigo_si_pni = grupo.find('codigo_si_pni').text
                grupo_pai = None #TODO: verificar esse campo

                with transaction.atomic():
                    GrupoAtendimento.objects.update_or_create(
                        nome=nome,
                        defaults={
                            'visivel': visivel,
                            'fase': fase or '',
                            'codigo_si_pni': codigo_si_pni or '',
                            'grupo_pai': grupo_pai
                        }
                    )

            self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar grupos de atendimento: {e}'))
