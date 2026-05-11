import hashlib
import json



lista_socios = []


def cadastro_socio():
   print ("Bem vindo ao cadastro de usúarios do nosso sistema!")
   nome = input ("Por gentileza, digite seu nome: ")
   rent = input("Por favor informe sua renda mensal: ")
   while True:
    cpf = input("Digite seu CPF *Sem pontuações somente números.: ")
    if not cpf.isdigit():
        print ("Digite somente números para o seu cpf.")
        continue
    if len(cpf) != 11:
         print ("quantidade de caracteres incorreta.")
         continue
    break
    
   while True:
    senha = input("digite sua senha: ")
    if len (senha) < 8:
       print ("Senha muito curta. ")
       continue
    elif len(senha) > 32:   
       print ("senha muito longa. ")
       continue
    break

   
   lista_socios.append ({"nome": nome, "cpf" : cpf , "senha" : senha , "rent" : rent})
   print(lista_socios)
   print("usuário criado com sucesso, por gentileza realize o login")
   

def login ():
    print ("Seja bem vindo login de usuário! Por gentileza")
    nome = input ("Digite o seu usuário: ")
    cpf = input ("Digite seu CPF: ")
    senha = input ("Digite sua senha: ")
    for s in lista_socios:
        if s["cpf"] == cpf and s["senha"] == senha and s["nome"] == nome: 
            print ("Você foi logado com sucesso! Seja bem vindo.") 
            return 

    print ("Usuário não encontrado, tente novamente.")
    
    
      
while True: 
    print ("====== Menu Do Sistema do Torcedor SCCP =======")
    print ("-1 Cadastro de Sócio")
    print ("-2 Realizar Login")
    print ("-3 Simulação de venda de ingresso.")
    print ("- 0 Sair ")
    
    opção  =  input ("Digite a opção desejada: ")
    
    if opção == "1":
       cadastro_socio ()
    
    elif opção == "2":
        login()
    
    elif opção == "3":
        pass
     
    elif opção == "0":
        print ("Obrigado por usar nosso programa, até logo!")
        break
    
    else: 
        print("Opção invalida, tente novamente.")
    
# salvar arquivos em json, lista de dicionarios dos usuarios no json . dump extensao de escrita json            