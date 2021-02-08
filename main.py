import os
import random
import sqlite3 as sql
from database.magic_cards import card_library
from database.deck_builder.deck_build import DeckBuild

class BeginningPhase():
    def upkeep():
        pass

    def untap():
        pass

    def draw():
        def seven():
            pass
        def one():
            pass
    def mully():
        pass
    pass

class MainPhase():
    pass

class CombatPhase():
    pass

class EndPhase():
    pass

class SearchFor():
    # class intended to search library for a card to place in hand or battlefield
    pass

class PlaceOnBattlefield():
    def side1():
        global board
        global p1
        for k,v in enumerate(p1['Player Hand']):
            print(f"{k} | {v['name']}")
            print()
        place_card = input('Choose a number to place the card. ')
        try:
            place_card = int(place_card)
        except:
            pass
        if p1['Player Hand'][place_card]['type_line'][:8] == 'Creature':
            board['Side 1'].append({'card':p1['Player Hand'][place_card],'Summoning Sickness?':True,'Tapped?':False})
        else:
            board['Side 1'].append({'card':p1['Player Hand'][place_card],'Summoning Sickness?':False,'Tapped?':False})

def put_in_cz(deck,commander):
    for i in deck:
        if commander.lower() in i['name'].lower():
            c = i
            deck.remove(i)
    return c

def shuffle(deck):
    random.shuffle(deck)

def roll_dice():
    dice = []
    for i in range(1,21):
        dice.append(i)
    random.shuffle(dice)
    # print(dice)
    roll = dice[0]

    return roll

def check_winner(players):
    for i in players:
        if i['Life Total'] <= 0:
            playing = False
    return playing

magic_lib = card_library.cards_db()
for i in range(8):
    print()
print("Library Populated")
print('Items in Library: ' + str(len(magic_lib)))
game_modes = {'1':'Player vs Player','2':'Two vs Two','3':'Multi: Four Players Free For All','4':'Create Deck','q':'Quit Game'}
print()
print("Welcome to Magic the Gathering Online!!!")
print()
print()
print('______GAME MODES______')
print()
print()

for k,v in enumerate(game_modes):
    print(f"  {v} | {game_modes[v]}")
    print()

print()
print()
select = input('What mode do you want to play? ')
selecting = True
while selecting:
    if select == '1':
        print('Player One...')
        p1_deck,p1_commander = DeckBuild.deck_manager()
        p1_commander = put_in_cz(p1_deck,p1_commander)
        shuffle(p1_deck)
        p1 = {'Command Zone':p1_commander,'Life Total':30,'Land Played?':False,'Turns Played':0,'Turn_Assign':0,'Mana':{'colorless':0,'island':0,'forest':0,'swamp':0,'mountain':0,'plains':0},'Player Hand':[],'Deck':p1_deck,'Graveyard':{'grave':[],'exiled':[]},}
        p1_mana_total = int(p1['Mana']['colorless'] + p1['Mana']['forest']+ p1['Mana']['island'] + p1['Mana']['swamp'] + p1['Mana']['mountain'] + p1['Mana']['plains'])
        print('Player Two...')
        p2_deck,p2_commander = DeckBuild.deck_manager()
        p2_commander = put_in_cz(p2_deck,p2_commander)
        shuffle(p2_deck)
        p2 = {'Command Zone':p2_commander,'Life Total':30,'Land Played?':False,'Turns Played':0,'Turn_Assign':0,'Mana':{'colorless':0,'island':0,'forest':0,'swamp':0,'mountain':0,'plains':0},'Player Hand': [],'Deck':p2_deck,'Graveyard':{'grave':[],'exiled':[]}}
        p2_mana_total = int(p2['Mana']['colorless'] + p2['Mana']['forest']+ p2['Mana']['island'] + p2['Mana']['swamp'] + p2['Mana']['mountain'] + p2['Mana']['plains'])
        board = {'Side 1': [],'Side 2': [],'Stack':[]}
        for i in range(30):
            print()
        print(str(p1['Command Zone']['name']) + ' V.S. ' + str(p2['Command Zone']['name']))
        for i in range(3):
            print()
        rolling = True
        while rolling:
            p1_roll = input('Player One Press Enter To Roll Dice. ')
            if p1_roll == "":
                p1_roll = roll_dice()
                print("You rolled : " + str(p1_roll))
            p2_roll = input('Player Two Press Enter to Roll Dice. ')
            if p2_roll == "":
                p2_roll = roll_dice()
                print("You rolled : " + str(p2_roll))
            if p1_roll > p2_roll:
                p2['Turn_Assign'] = 1
                print(f"Player with {str(p1['Command Zone']['name'])} goes first")
                rolling = False
            elif p1_roll < p2_roll:
                p1['Turn_Assign'] = 1
                print(f"Player with {str(p2['Command Zone']['name'])} goes first")
                rolling = False
            else:
                print("Roll Again")
        for i in range(3):
            print()
        print()
        print('*********************BOARD*********************')
        print()
        print(f"{str(p1['Command Zone']['name'])}  |      {board['Side 1']}")
        print()
        print("_______________________________________________")
        print()
        print(f"{str(p2['Command Zone']['name'])}  |      {board['Side 2']}")
        print()
        print()
        print(f"Player One Life: {p1['Life Total']}     |     Player Two Life: {p2['Life Total']}")

        playing = True
        while playing:
            players = [p1,p2]
            for i in players:
                if i['Turn_Assign'] == 0:
                    # player 1 goes through game phases
                    pass
                check_winner(players)
                if i['Turn_Assign'] == 1:
                    # Player 2 goes through game phases
                    pass
                check_winner(players)
            pass

        selecting = False
    elif select == '2':
        pass
    elif select == '3':
        pass
    elif select == '4':
        magic_cards = DeckBuild.card_library()
        deck,commander = DeckBuild.deck_manager()
    elif select == 'q':
        selecting = False
        break
    else:
        print('Please try a press a key in menu.')
        continue
