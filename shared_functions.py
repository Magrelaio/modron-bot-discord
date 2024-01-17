'''Arquivo para criação de diversas funções que se comunicam entre varios comandos - Principalmente os de inventario
'''

import json
import numpy as np
import re

def formatar_inventario(inventario):
    return "\n".join([f"{item} ({quantidade} unidades)" for item, quantidade in inventario.items()])

def load_inventory():
    try:
        with open('inventory.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return {}

def save_inventory(inventory):
    with open('inventory.json', 'w', encoding='utf-8') as file:
        json.dump(inventory, file, indent=4)

def processar_rolagem(expressao):
    dice_number, dice_type, operador, bonus = separar_operadores(expressao)
    return processar_expressao(dice_number, dice_type, operador, bonus)
        
''' criação de função para correção de codigo no original. - não vou mexer nisso ainda, irei terminar primeiro o inventario
def sum(message):
    try:
        dice_type, *bonus_list = split_message[1].split('+')
        bonus = sum(int(b) for b in bonus_list)
    except:
        bonus = 0
OLHA ABAIXO.
'''

def processar_expressao(dice_number, dice_type, operador, bonus):
    if int(dice_type) >= 201:
        return f'Número de lados muito alto! Tente um numero mais baixo por favor (máximo de 200)'
    
    if int(dice_type) <= 0:
        return 'Numero de lados inválido. Você precisa rolar um numero acima de 1!'

    rolls = sorted(np.random.choice(np.arange(1, int(dice_type) + 1)) for _ in range(dice_number))

    if int(dice_number) >= 26:
        return 'Numero de dados muito alto! tente um numero mais baixo por favor (máximo de 25)'

    if int(dice_number) <= 0:
        return 'Numero de dados inválido. Você precisa rolar um numero acima de 1! - ou deixe em branco como "d20"'

    roll_str = f"{dice_number}d{dice_type}"

    total_roll = sum(rolls) + abs(bonus) if operador == '+' else  sum(rolls)
        
    total_roll = sum(rolls) - abs(bonus) if operador == '-' else sum(rolls)
    
    total_roll = sum(rolls) * abs(bonus) if operador == '*' else sum(rolls)
    
    total_roll = sum(rolls) / abs(bonus) if operador == '/' else sum(rolls)
    
    roll_str += f"{operador} {bonus}" 
#aqui ele só está retornando 3 pq sintetizei a expressão, mas eram p ser 4 valores
    return rolls, total_roll, roll_str

'''def separar_operadores(expressao):
    for operador in ['+', '-', '*', '/']:
        partes = re.compile(r'(\d|[+\-*/])')
        if operador in expressao:
            partes = expressao.split(operador, 1)
            return partes[0], operador, partes[1]'''

def separar_operadores(expressao):
    padrao = re.compile(r'(\d*)d(\d+)([+\-*/]?)(\d*)')

    correspondencias = padrao.match(expressao)

    if correspondencias:
        dice_number = int(correspondencias.group(1)) if correspondencias.group(1) else 1
        dice_type = int(correspondencias.group(2))
        operador = correspondencias.group(3) if correspondencias.group(3) else ''
        bonus = int(correspondencias.group(4)) if correspondencias.group(4) else ''
        print(f'{dice_number, dice_type, operador, bonus}')

        return dice_number, dice_type, operador, bonus
    else:
        return