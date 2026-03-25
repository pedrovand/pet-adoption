from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Pet(models.Model):
    # Opções para os campos de escolha (Choices) - Isso cria o "dropdown" no formulário
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('adotado', 'Adotado'),
        ('em_tratamento', 'Em Tratamento'),
    ]

    # Campos seguindo a estrutura do seu SQL original
    nome = models.CharField(max_length=100) 
    data_entrada = models.DateField(default=timezone.now)
    idade = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cor = models.CharField(max_length=50, null=True, blank=True)
    descricao = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='disponivel'
    )
    
    # Relacionamento com o usuário do sistema (FK)
    # PROTECT impede que um pet seja deletado se o usuário for removido
    usuario_cadastro = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='pets_cadastrados'
    )

    # Isso faz o nome do gato aparecer bonitinho na lista do painel Admin
    def __str__(self):
        return f"{self.nome} ({self.status})"