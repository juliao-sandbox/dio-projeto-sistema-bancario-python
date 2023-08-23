from datetime import datetime

menu: str = """

-----------------
    BANCO DIO
-----------------
[d] Depositar
[s] Sacar
[e] Extrato
-----------------
[q] Sair

=> """

saldo: float = 0
extrato: str = ""
contador_saques: int = 0
LIMITE_DIARIO: float = 500.0
LIMITE_SAQUES: int = 3


def depositar(valor: float) -> None:
    global extrato
    global saldo

    if valor > 0:
        saldo += valor
        extrato += f" * Depósito R$ {valor:.2f}\n"
        print(f" * Você depositou {valor:.2f}. Seu saldo agora é: R$ {saldo:.2f}")
    else:
        print(" * Valor inválido, tente novamente digitando um valor maior do que zero.")


def sacar(valor: float) -> None:
    global extrato
    global contador_saques
    global saldo

    if valor > saldo:
        print(f" * Operação falhou! O saldo é insuficiente, saldo atual: R$ {saldo:.2f}")
    elif contador_saques >= LIMITE_SAQUES:
        print(f" * Operação falhou! Você atingiu o limite de {LIMITE_SAQUES} saques diários.")
    elif valor > LIMITE_DIARIO:
        print(f" * Operação falhou! O valor é maior do que o limite diário de R$ {LIMITE_DIARIO:.2f}")
    elif valor > 0:
        saldo -= valor
        contador_saques += 1
        extrato += f" * Saque R$ {valor:.2f}\n"
        print(f" * Você sacou {valor:.2f}. Seu saldo agora é: R$ {saldo:.2f}")
    else:
        print(" * Valor inválido, tente novamente digitando um valor maior do que zero.")


def mostrar_extrato() -> None:
    global extrato
    global saldo
    LARGURA: int = 30

    print(" EXTRATO ".center(LARGURA, "="))
    if extrato:
        print(extrato)
    else:
        print(" -- Nenhuma movimentação --")
    print(f"\n  Saldo: R$ {saldo:.2f}")
    print("".center(LARGURA, "="))


def ler_valor(mensagem: str) -> float:
    try:
        valor: float = float(input(mensagem))
        if valor > 0:
            return valor
        else:
            raise ValueError
    except ValueError:
        print(" * Valor inválido, você deve digitar um valor numérico maior que zero. *")
    return 0

def sair() -> None:
    HORA_AMANHECER: int = 6
    HORA_MEIO_DIA: int = 12
    HORA_ANOITECER: int = 18
    HORA_AGORA: int =  datetime.now().hour

    if HORA_AMANHECER <= HORA_AGORA < HORA_MEIO_DIA:
        mensagem: str = "tenha um bom dia!"
    elif HORA_MEIO_DIA <= HORA_AGORA < HORA_ANOITECER:
        mensagem: str = "tenha uma boa tarde!"
    else:
        mensagem: str = "tenha uma boa noite!"
    
    print(f"-- Até logo, {mensagem}")


def main() -> None:
    while True:
        opcao: str = input(menu).lower()

        if opcao == "d":
            print("-- DEPÓSITO --")
            valor: float = ler_valor("Digite o valor que deseja depositar: ")
            if valor > 0:
                depositar(valor)
        elif opcao == "s":
            print("-- SAQUE --")
            valor: float = ler_valor("Digite o valor que deseja sacar: ")
            if valor > 0:
                sacar(valor)
        elif opcao == "e":
            mostrar_extrato()
        elif opcao == "q":
            sair()
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
