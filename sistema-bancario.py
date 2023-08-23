import textwrap
from datetime import datetime


def menu(nome_banco: str) -> str:
    LARGURA: int = 30

    menu: str = f"""
    {"-" * LARGURA}
    {nome_banco.center(LARGURA, " ")}
    {"-" * LARGURA}
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [lu]\tListar usuários
    [nc]\tNova conta
    [lc]\tListar contas
    {"-" * LARGURA}
    [q]\tSair
    => """

    return input(textwrap.dedent(menu)).lower()


def depositar(saldo: float, valor: float, extrato: str) -> (float, str):
    if valor > 0:
        saldo += valor
        extrato += f" * Depósito R$ {valor:.2f}\n"
        print(f" * Você depositou R$ {valor:.2f}. Seu saldo agora é: R$ {saldo:.2f}")
    else:
        print(" * Valor inválido, tente novamente digitando um valor maior do que zero.")
    return saldo, extrato


def sacar(*, saldo: float, valor: float, extrato: str, limite_diario: float, contador_saques: int, limite_saques: int) -> (float, str):
    if valor > saldo:
        print(f" * Operação falhou! O saldo é insuficiente, saldo atual: R$ {saldo:.2f}")
    elif contador_saques >= limite_saques:
        print(f" * Operação falhou! Você atingiu o limite de {limite_saques} saques diários.")
    elif valor > limite_diario:
        print(f" * Operação falhou! O valor é maior do que o limite diário de R$ {limite_diario:.2f}")
    elif valor > 0:
        saldo -= valor
        contador_saques += 1
        extrato += f" * Saque R$ {valor:.2f}\n"
        print(f" * Você sacou R$ {valor:.2f}. Seu saldo agora é: R$ {saldo:.2f}")
    else:
        print(" * Valor inválido, tente novamente digitando um valor maior do que zero.")
    return saldo, extrato, contador_saques


def exibir_extrato(saldo: float, *, extrato: str) -> None:
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


def criar_usuario(usuarios: list) -> None:
    cpf: str = input("Informe o CPF (somente números): ")
    usuario: str = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(" * Já existe usuário com este CPF!")
        return

    nome: str = input("Informe o nome completo: ")
    data_nascimento: str = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco: str = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    novo_usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    usuarios.append(novo_usuario)

    print(" * Usuário cadastrado!")
    exibir_usuario(novo_usuario)


def exibir_usuario(usuario: dict) -> None:
    linha = f"""
        CPF: {usuario['cpf']}
        Nome: {usuario['nome']}
        Data de nascimento: {usuario['data_nascimento']}
        Endereço: {usuario['endereco']}
    """
    print("-" * 30, end="")
    print(textwrap.dedent(linha))


def listar_usuarios(usuarios: list) -> None:
    print(" * Todas os usuários cadastrados:")
    if usuarios:
        for usuario in usuarios:
            exibir_usuario(usuario)
    else:
        print(" -- Nenhum usuário cadastrado --")


def filtrar_usuario(cpf: str, usuarios: list) -> None:
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_conta(agencia: str, numero_conta: str, usuarios: list) -> str:
    cpf: str = input("Informe o CPF do usuário: ")
    usuario: str = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(" * Conta criada!")
        nova_conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        exibir_conta(nova_conta)
        return nova_conta
    print(" * Usuário não encontrado, verifique as informações fornecidas!")


def exibir_conta(conta: dict) -> None:
    linha = f"""
        Agência:\t{conta['agencia']}
        Conta:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
    """
    print("-" * 30, end="")
    print(textwrap.dedent(linha))


def listar_contas(contas: list) -> None:
    print(" * Todas as contas cadastradas:")
    if contas:
        for conta in contas:
            exibir_conta(conta)
    else:
        print(" -- Nenhum conta cadastrada --")


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
    NOME_BANCO = "BANCO DIO"
    AGENCIA = "0001"
    LIMITE_DIARIO: float = 500.0
    LIMITE_SAQUES: int = 3

    saldo: float = 0
    extrato: str = ""
    contador_saques: int = 0

    usuarios: list = []
    contas: list = []

    while True:
        opcao: str = menu(NOME_BANCO)

        if opcao == "d":
            print("-- DEPÓSITO --")
            valor: float = ler_valor("Digite o valor que deseja depositar: ")
            if valor > 0:
                saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "s":
            print("-- SAQUE --")
            valor: float = ler_valor("Digite o valor que deseja sacar: ")
            if valor > 0:
                saldo, extrato, contador_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite_diario=LIMITE_DIARIO,
                    contador_saques=contador_saques,
                    limite_saques=LIMITE_SAQUES,
                )
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "lu":
            listar_usuarios(usuarios)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            sair()
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
