print("Calculadora de juros\n")

def calcular_juros(capital, taxa, tempo, composto=False):
    if composto:
        montante = capital * (1 + taxa / 100) ** tempo
    else:
        montante = capital + (capital * (taxa / 100) * tempo)
    juros = montante - capital
    return juros, montante

while True:
    try:
        tipo_juros = int(input("Insira o tipo de juros:\n1 - Juros Simples\n2 - Juros Compostos\nDigite 1 ou 2: "))
        if tipo_juros not in [1, 2]:
            raise ValueError("\nOpção inválida. Digite 1 ou 2.\n")
        capital = float(input("\nDigite o capital (R$): "))
        taxa = float(input("Digite a taxa de juros (%): "))
        tempo = int(input("Digite o tempo (em meses): "))
        if capital < 0 or taxa < 0 or tempo < 0:
            raise ValueError("\nOs valores devem ser positivos.\n")
        composto = tipo_juros == 2
        juros, montante = calcular_juros(capital, taxa, tempo, composto)
        tipo = "Compostos" if composto else "Simples"
        print(f"\nJuros {tipo}: R$ {juros:.2f}\nMontante: R$ {montante:.2f}\n")
        break
    except ValueError as e:
        print(e)
