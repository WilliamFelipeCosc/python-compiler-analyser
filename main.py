print("Calculadora de juros\n")

def calcular_juros_simples(capital, taxa, tempo):
  juros = capital * (taxa / 100) * tempo
  montante = capital + juros
  return juros, montante

def calcular_juros_compostos(capital, taxa, tempo):
  montante = capital * (1 + taxa / 100) ** tempo
  juros = montante - capital
  return juros, montante

while True:
  try:
    print("Insira o tipo de juros:")
    print("1 - Juros Simples")
    print("2 - Juros Compostos")
    tipo_juros = int(input("Digite 1 ou 2: "))

    if tipo_juros not in [1, 2]:
      raise ValueError("\nOpção inválida. Digite 1 ou 2.\n")
    else:
      break
  except ValueError as e:
    print(e)
    continue

while True:
  try:
    capital = float(input("\nDigite o capital (R$): "))
    taxa = float(input("Digite a taxa de juros (%): "))
    tempo = int(input("Digite o tempo (em meses): "))

    if capital < 0 or taxa < 0 or tempo < 0:
      raise ValueError("\nOs valores devem ser positivos.\n")

    if tipo_juros == 1:
      juros, montante = calcular_juros_simples(capital, taxa, tempo)
      print(f"\nJuros Simples: R$ {juros:.2f}")
      print(f"Montante: R$ {montante:.2f}\n")
    elif tipo_juros == 2:
      juros, montante = calcular_juros_compostos(capital, taxa, tempo)
      print(f"\nJuros Compostos: R$ {juros:.2f}")
      print(f"Montante: R$ {montante:.2f}\n")
    break
  except ValueError as e:
    print(e)
