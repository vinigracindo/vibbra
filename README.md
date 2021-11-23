# Vibbra! - Ecommerce Venda e Troca

# 1. Avaliação do Escopo
Inicialmente, fiz uma avaliação geral do escopo do projeto e enviei as dúvidas iniciais.
Fiz alterações nos endpoints de Frete. O webservice do correios exige que sejam enviandos dados
refirente ao item que será enviado.

Endpoint descrito no escopo do projeto
```console
URI sugerida: /api/v{n}/deal/{ID}/deliveries
Public: NÃO
Tipo: POST
Requests: { “user_id": INT }
Return Success: { “delivery": OBJECT }
Return Fail: { "message" : STRING }
```

Endpoint alterado 
```console
URI sugerida: /api/v{n}/deal/{ID}/deliveries
Public: NÃO
Tipo: POST
Requests: { "weight": Double,  "format": ENUM ("caixa", "rolo", "envelope"), "width": Double, "height": Double, "length": Double}
Return Success: { “delivery": OBJECT }
Return Fail: { "message" : STRING }
```

Removi o user_id pois existe um usuário logado na sessão (rota não pública) e existe o usuário de destino no deal que é passado pela url.

Obs.: Tomei a liberdade de realizar essa modificação porque enviei e-mail e não obtive respostas.

# 2. Estimativa em horas de desenvolvimento de Todo o projeto/atividades descritas no escopo.
Sempre estimo 1 hora por endpoints de baixa complexidade (Endpoint que faz uma consulta ao DB e retorna o resultado),
A cada endpoint acrescento 45 minutos para testes e documentação.

Adiciono ao final do projeto +4 horas (projetos desse tamanho) para configuração de deploy com docker ou terraform.

Total: 42,5 horas.

# 3. Estimativa em DIAS do prazo de entrega
Ser freelancer não é meu trabalho principal, então não me dedico 8 horas por dia em projetos Freela.
Minha disponibilidade são 3h por dia (18 horas semanais) garantidas.

Tempo estimado para esse projeto: 7 dias (máximo).

# Descrição Técnica

O projeto contém um banco de dados com dados preenchidos para testes.

Para testar a autenticação SSO, foi criado um token para o usuário admin.
Token: 4005721aca633c59c9a40203bf2ad641861fb4e9

Obs.: Estou adicionando a pasta media no git para fins de testes. Como falei, estou enviando um banco de dados de testes já preenchido.

## Requirements
1. Django >= 3.2
2. Python >= 3.8
3. PostgresSQL >= 9.4

## How to develop?
1. Clone
2. Create a virtual environment
3. Active virtual environment
4. Install projects dependencies
5. Run migrations
6. Run tests
7. Run server

### Linux
```console
git clone https://git.vibbra.com.br/vinnicyus/vibbra-ecommerce.git vibbra-ecommerce-api
cd vibbra-ecommerce-api
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Deploy com Docker

1. Clone o projeto e execute o docker compose
```console
git clone https://git.vibbra.com.br/vinnicyus/vibbra-ecommerce.git
cd vibbra-ecommerce
docker-compose up -d
```

Serviço ficará disponível em:
http://localhost:8080

ACESSE A DOCUMENTAÇÃO DA API EM:
http://localhost:8080/swagger/

Usuários para testes:

admin / admin

user1 / 123456

user2 / 123456