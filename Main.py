import hashlib
import json


lista_socios = []
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

LIMITE_RENDA_SOCIAL = 1518.00

def carregar_dados():
   global lista_socios
   try:
      with open("socios.json", "r", encoding="utf-8") as arquivo:
         lista_socios = json.load(arquivo)
         print("Os dados foram carregados com sucesso!")
   except FileNotFoundError:
      pass

def salvar_dados():
   with open("socios.json", "w", encoding="utf-8") as arquivo:
      json.dump(lista_socios, arquivo, ensure_ascii=False, indent=4)

def gerar_hash(senha):
   return hashlib.sha256(senha.encode()).hexdigest()

def cadastro_socios():
   print("\nBem vindo ao cadastro de usuários do nosso sistema!")
   nome = input("Por gentileza, digite seu nome: ")

   while True:
      try:
         renda = float(input("Por favor informe sua renda mensal: "))
         break
      except ValueError:
         print("Digite um valor numérico válido.")

   while True:
      cpf = input("Digite seu CPF (Sem pontuações somente números): ")
      if not cpf.isdigit():
         print("Digite somente números para o seu CPF.")
         continue
      if len(cpf) != 11:
         print("Quantidade de caracteres incorreta.")
         continue
      break

   while True:
      senha = input("Digite sua senha: ")
      if len(senha) < 8:
         print("Senha muito curta.")
         continue
      elif len(senha) > 32:
         print("Senha muito longa.")
         continue
      break

   print("\n Planos disponíveis:")
   print(" ouro -> 100% de desconto no ingresso")
   print(" prata -> 50% de desconto no ingresso")
   print(" bronze -> 20% de desconto no ingresso")
   if renda <= LIMITE_RENDA_SOCIAL:
      print(" social -> 80% de desconto (você é elegível ao plano social!)")
   else:
      print(" (plano social indisponível para sua renda).")

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

   lista_socios.append(
      {
         "nome": nome,
         "cpf": cpf,
         "senha": senha_hash,
         "renda": renda,
         "plano": plano,
         "mensalidade": True,
      }
   )

   salvar_dados()
   print("Usuário criado com sucesso, por gentileza realize o login.")


def login():
   global usuario_logado
   print("\nSeja bem vindo, por gentileza realize o seu login de usuário!")
   nome = input("Digite o seu nome: ")
   cpf = input("Digite seu CPF: ")
   senha = input("Digite sua senha: ")

   senha_hash = gerar_hash(senha)

   for s in lista_socios:
      if s["cpf"] == cpf and s["senha"] == senha_hash and s["nome"] == nome:
         usuario_logado = s
         print(f"Você foi logado com sucesso! Seja bem vindo, {nome}.")
         return

   print("Usuário não encontrado, tente novamente.")


def simular_venda():
   if usuario_logado is None:
      print("Você precisa fazer o login antes de comprar ingressos.")
      return
   if not usuario_logado["mensalidade"]:
      print("Sua mensalidade está em atraso. Regularize para comprar ingressos.")
      return

   print("\n Setores disponíveis - Neo Química Arena:")
   for key, setor in SETORES.items():
      print(f"{key} - {setor['nome']:<25} R$ {setor['valor']:.2f}")

   while True:
      escolha = input("Escolha o setor desejado: ")
      if escolha not in SETORES:
         print("Setor inválido.")
         continue
      break

   setor_escolhido = SETORES[escolha]
   valor_base = setor_escolhido["valor"]
   plano = usuario_logado["plano"]
   descontos = {
      "ouro": 1.00,
      "social": 0.80,
      "prata": 0.50,
      "bronze": 0.20,
   }
   percentual = descontos[plano]
   desconto = valor_base * percentual
   valor_final = valor_base - desconto

   print("\n ============== TICKET DE INGRESSO ================")
   print(f" Sócio:                 {usuario_logado['nome']}")
   print(f" Plano:                 {plano.capitalize()}")
   print(f" Setor:                 {setor_escolhido['nome']}")
   print(f" Valor base:          R$ {valor_base:.2f}")
   print(f" Desconto:            R$ {desconto:.2f}  ({int(percentual * 100)}%)")
   print(f" Valor Final:         R$ {valor_final:.2f}")
   print(" ==================================================\n")


carregar_dados()

while True:
   print("====== Menu Do Sistema do Torcedor Corinthians =======")
   print("- 1 Cadastro de Sócio")
   print("- 2 Realizar Login")
   print("- 3 Simulação de venda de ingresso.")
   print("- 0 Sair")

   opcao = input("Digite a opção desejada: ")

   if opcao == "1":
      cadastro_socios()

   elif opcao == "2":
      login()

   elif opcao == "3":
      simular_venda()

   elif opcao == "0":
      print("Obrigado por usar nosso programa, até logo!")
      break

   else:
      print("Opção inválida, tente novamente.")
