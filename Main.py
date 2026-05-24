import hashlib
import json

# ============================================================
# Sistema de Gestão de Sócio Torcedor - Sport Club Corinthians
# ============================================================

# Lista de soocios global para armazenar os dados dos sócios, será carregada do arquivo JSON.
lista_socios = []

 
# Variável que armazena o sócio atualmente logado no sistema.
usuario_logado = None

# criação de setores com valores dos ingressos fonte: corinthians.com.br

SETORES = {
   "1": {"nome": "Norte", "valor": 80.00},
   "2": {"nome": "Sul", "valor": 150.00},
   "3": {"nome": "Leste Superior Corner", "valor": 100.00},
   "4": {"nome": "Leste Superior Lateral", "valor": 120.00},
   "5": {"nome": "Leste Superior Central", "valor": 125.00},
   "6": {"nome": "Leste Inferior Corner", "valor": 130.00},
   "7": {"nome": "Leste Inferior Lateral", "valor": 140.00},
   "8": {"nome": "Leste Inferior Central", "valor": 170.00},
   "9": {"nome": "Oeste Superior", "valor": 170.00},
}

# Limite de renda mensal para elegibilidade ao plano social.
LIMITE_RENDA_SOCIAL = 1518.00

#função: carregar_dados
# Carrega os dados dos sócios salvos no arquivo socios.json caso o arquivo não exista, o sistema inicia com lista vazia.

def carregar_dados():
   global lista_socios
   try:
      with open("socios.json", "r", encoding="utf-8") as arquivo:
         lista_socios = json.load(arquivo)
         print("Os dados foram carregados com sucesso!")
   except FileNotFoundError:
      pass

# função: salvar_dados Salva a lista de sócios atualizada no arquivo socios.json, garantindo a persistência dos dados entre execuções.
def salvar_dados():
   with open("socios.json", "w", encoding="utf-8") as arquivo:
      json.dump(lista_socios, arquivo, ensure_ascii=False, indent=4)

#função: gerar_hash Recebe a senha em texto puro e retorna seu hash SHA-256, para que o armazenamento da senha original no arquivo seja evitado.
def gerar_hash(senha):
   return hashlib.sha256(senha.encode()).hexdigest()
 
# função: cpf_ja_cadastrado verifica se o CPF informado já existe na lista de sócios, impedindo cadastros duplicados no sistema.

def cpf_ja_cadastrado(cpf):
   for socio in lista_socios:
      if socio["cpf"] == cpf:
         return True
   return False

#função cadastro_socios: Responsável por realizar o cadastro de um novo sócio, Coleta nome, renda, CPF, plano e senha do usuário, valida as entradas e salva os dados do sócio no arquivo JSON.
def cadastro_socios():
   print("\nBem vindo ao cadastro de usuários do nosso sistema!")
   nome = input("Por gentileza, digite seu nome: ")
#valida a renda mensal
   while True:
      try:
         renda = float(input("Por favor informe sua renda mensal: "))
         break
      except ValueError:
         print("Digite um valor numérico válido.")
# valida o cpf e define que so aceita digitos e 11 caracteres e sem duplicidade
   while True:
      cpf = input("Digite seu CPF (Sem pontuações somente números): ")
      if not cpf.isdigit():
         print("Digite somente números para o seu CPF.")
         continue
      if len(cpf) != 11:
         print("Quantidade de caracteres incorreta.")
         continue
      if cpf_ja_cadastrado(cpf):
         print("Este CPF já está cadastrado no sistema.")
         continue
      break
   
   
   
   # valida a senha minimo de 8 e maximo de 32 caracteres
   while True:
      senha = input("Digite sua senha: ")
      if len(senha) < 8:
         print("Senha muito curta.")
         continue
      elif len(senha) > 32:
         print("Senha muito longa.")
         continue
      break

  #Exibe os planos disponiveis de acordo com a renda
   print("\n Planos disponíveis:")
   print(" ouro -> 100% de desconto no ingresso")
   print(" prata -> 50% de desconto no ingresso")
   print(" bronze -> 20% de desconto no ingresso")
   if renda <= LIMITE_RENDA_SOCIAL:
      print(" social -> 80% de desconto (você é elegível ao plano social!)")
   else:
      print(" (plano social indisponível para sua renda).")
  
   # Bloqueio do plano para renda que ultrapasse o limite.
   
   while True:
      plano = input("Escolha seu plano: ").strip().lower()
      if plano == "social" and renda > LIMITE_RENDA_SOCIAL:
         print("Sua renda não é elegível para o plano social.")
         continue
      if plano not in ["ouro", "prata", "bronze", "social"]:
         print("Plano inválido. Escolha entre: ouro, prata, bronze ou social")
         continue
      break

   # geração de hash para não salvar a senha pura
   senha_hash = gerar_hash(senha)

  # Adiciona o novo socio a lista e também inicia um contador para ver a quantidade de ingressos adiquirido por cada pessoa.  
   lista_socios.append(
      {
         "nome": nome,
         "cpf": cpf,
         "senha": senha_hash,
         "renda": renda,
         "plano": plano,
         "mensalidade": True,
         "ingressos_comprados": 0,
      }
   )

   salvar_dados()
   print("Usuário criado com sucesso, por gentileza realize o login.")

# função login autentica o sócio verificando nome, CPF e hash da senha se os dados forem válidos, define o usuário logado globalmente.

def login():
   global usuario_logado
   print("\nSeja bem vindo, por gentileza realize o seu login de usuário!")
   nome = input("Digite o seu nome: ")
   cpf = input("Digite seu CPF: ")
   senha = input("Digite sua senha: ")
   #Gera o hash da senha informada para comparar com o hash armazenado no arquivo JSON.
   senha_hash = gerar_hash(senha)

   #percorre a lista buscando correspondencia para liberar o login
   for s in lista_socios:
      if s["cpf"] == cpf and s["senha"] == senha_hash and s["nome"] == nome:
         usuario_logado = s
         print(f"Você foi logado com sucesso! Seja bem vindo, {nome}.")
         return

   print("Usuário não encontrado, tente novamente.")

# função: simular_venda Simula a compra de um ingresso para o sócio logado valida login e situação da mensalidade antes de prosseguir.
#Aplica o desconto conforme o plano do sócio e exibe o ticket incrementa o contador de ingressos comprados pelo sócio.
def simular_venda():
   # Bloqueia o acesso se nenhum sócio estiver logado
   if usuario_logado is None:
      print("Você precisa fazer o login antes de comprar ingressos.")
      return
    
     # Bloqueia a compra se a mensalidade estiver em atraso
   if not usuario_logado["mensalidade"]:
      print("Sua mensalidade está em atraso. Regularize para comprar ingressos.")
      return

   # Exibe os setores disponíveis com seus valores base
   print("\n Setores disponíveis - Neo Química Arena:")
   for key, setor in SETORES.items():
      print(f"{key} - {setor['nome']:<25} R$ {setor['valor']:.2f}")

   # Valida a escolha do setor
   while True:
      escolha = input("Escolha o setor desejado: ")
      if escolha not in SETORES:
         print("Setor inválido.")
         continue
      break

   # Calcula o valor com desconto conforme o plano do sócio
   setor_escolhido = SETORES[escolha]
   valor_base = setor_escolhido["valor"]
   plano = usuario_logado["plano"]
   
   # Tabela de percentuais de desconto por plano
   descontos = {
      "ouro": 1.00,
      "social": 0.80,
      "prata": 0.50,
      "bronze": 0.20,
   }
   percentual = descontos[plano]
   desconto = valor_base * percentual
   valor_final = valor_base - desconto
   
   # Incrementa o contador de ingressos do sócio logado e salva
   usuario_logado["ingressos_comprados"] = usuario_logado.get("ingressos_comprados", 0) + 1
   salvar_dados()

   # Exibe o ticket de ingresso formatado
   print("\n ============== TICKET DE INGRESSO ================")
   print(f" Sócio:                 {usuario_logado['nome']}")
   print(f" Plano:                 {plano.capitalize()}")
   print(f" Setor:                 {setor_escolhido['nome']}")
   print(f" Valor base:          R$ {valor_base:.2f}")
   print(f" Desconto:            R$ {desconto:.2f}  ({int(percentual * 100)}%)")
   print(f" Valor Final:         R$ {valor_final:.2f}")
   print(" ==================================================\n")

#função : listar_socios exibe todos os sócios cadastrados no sistema com suas informações principais (sem exibir senha ou hash).
def listar_socios():
   if not lista_socios:
      print("Nenhum sócio cadastrado ainda.")
      return

   print("\n========== SÓCIOS CADASTRADOS ==========")
   for i, s in enumerate(lista_socios, start=1):
      mensalidade_status = "Em dia" if s["mensalidade"] else "Em atraso"
      ingressos = s.get("ingressos_comprados", 0)
      print(f"\n Sócio #{i}")
      print(f"  Nome:       {s['nome']}")
      print(f"  CPF:        {s['cpf']}")
      print(f"  Plano:      {s['plano'].capitalize()}")
      print(f"  Mensalidade:{mensalidade_status}")
      print(f"  Ingressos:  {ingressos}")
   print("========================================\n")

# Inicialização: carrega os dados salvos ao iniciar o sistema
carregar_dados()


# MENU PRINCIPAL: loop principal do sistema com as opções disponíveis para o usuário interagir com o programa.
while True:
   print("====== Menu Do Sistema do Torcedor Corinthians =======")
   print("- 1 Cadastro de Sócio")
   print("- 2 Realizar Login")
   print("- 3 Simulação de venda de ingresso.")
   print("- 4 Listar sócios cadastrados")
   print("- 0 Sair")

   opcao = input("Digite a opção desejada: ")

   if opcao == "1":
      cadastro_socios()

   elif opcao == "2":
      login()

   elif opcao == "3":
      simular_venda()
      
   elif opcao == "4":
      listar_socios()

   elif opcao == "0":
      print("Obrigado por usar nosso programa, até logo!")
      break

   else:
      print("Opção inválida, tente novamente.")
