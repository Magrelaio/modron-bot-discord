'''Arquivo para criação de diversas funções que se comunicam entre varios comandos - Principalmente os de inventario
'''

import json

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
        
''' criação de função para correção de codigo no original. - não vou mexer nisso ainda, irei terminar primeiro o inventario
def sum(message):
    try:
        dice_type, *bonus_list = split_message[1].split('+')
        bonus = sum(int(b) for b in bonus_list)
    except:
        bonus = 0
'''