# core/management/commands/create_default_admin.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Cria um superusuário padrão a partir de variáveis de ambiente, se ele não existir."

    def handle(self, *args, **kwargs):
        # Lê as credenciais das variáveis de ambiente que você já configurou no Render
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

        # Verifica se as variáveis foram definidas no Render
        if not all([username, password, email]):
            self.stdout.write(self.style.ERROR(
                "Por favor, configure as variáveis de ambiente DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD e DJANGO_SUPERUSER_EMAIL no Render."
            ))
            return

        # Verifica se o usuário já existe antes de tentar criar
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Criando superusuário '{username}'..."))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superusuário '{username}' criado com sucesso!"))
        else:
            self.stdout.write(self.style.WARNING(f"Superusuário '{username}' já existe. Nenhuma ação foi tomada."))
