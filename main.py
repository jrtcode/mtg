import os
import random
import sqlite3 as sql
from database.magic_cards import card_library
from database.deck_builder.deck_build import DeckBuild
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# import pygame
#create class to create window

class PlayerTurn():
    def __init__ (self,deck):
        self.deck = deck
    class Draw():
        def draw_seven(deck):
            for i in range(1,8):
                deck['Player Hand'].append(deck['Deck'][0])
                deck['Deck'].pop(0)
            return deck
        def draw_one(deck):
            deck['Player Hand'].append(deck['Deck'][0])
            deck['Deck'].pop(0)
            return deck
        def mully(deck):
            if deck['Mully Count'] == 0:
                print()
                for i,v in enumerate(deck['Player Hand']):
                    print(f"{i}  |  {v}")
                    print()
                x = input("Choose which cards you want to remove, separated with a comma no spaces. ")
                x = x.split(',')
                for i in range(len(x)+1):
                    x.append(int(i))
                    x.pop(0)
                for item in x:
                    deck['Player Hand'].pop(item)
                    deck['Deck'].append(item)
                while len(deck['Player Hand']) < 7:
                    PlayerTurn.Draw.draw_one(deck)
            elif deck['Mully Count'] >= 1:
                count = 0
                for item in deck['Player Hand']:
                    deck['Deck'].append(item)
                    count += 1
                print(count, deck['Player Hand'])
                deck['Player Hand'].clear()
                while len(deck['Player Hand']) < 7:
                    PlayerTurn.Draw.draw_one(deck)
            deck['Mully Count'] += 1
            return deck
    class BeginningPhase():
        def upkeep():
            pass

        def untap(deck,board):
            if deck['Player Turn'] == 0:
                for y in board['Side 1']:
                    if y['Tapped?'] == True:
                        y['Tapped?'] = False
            elif deck['Player Turn'] == 1:
                for y in board['Side 2']:
                    if y['Tapped?'] == True:
                        y['Tapped?'] = False
            elif deck['Player Turn'] == 2:
                for y in board['Side 3']:
                    if y['Tapped?'] == True:
                        y['Tapped?'] = False
            elif deck['Player Turn'] == 3:
                for y in board['Side 4']:
                    if y['Tapped?'] == True:
                        y['Tapped?'] = False
            return board

    class MainPhase():
        def tap(deck,board):
            if deck['Player Hand'] == 0:
                for i,v in enumerate(board['Side 1']):
                    print(f" {i} | {v}")
                    print()
                tap = input("What cards do you want to tap? ")
                tap = tap.split(',')
                for y in tap:
                    y = int(y)
                    board["Side 1"][y]["Tapped?"] = True
                    if board["Side 1"][y]['cmc'] =='Island':
                        deck['Mana']['island'] += 1
                    elif board["Side 1"][y]['cmc'] == 'Mountain':
                        deck['Mana']['mountain'] += 1
                    elif board["Side 1"][y]['cmc'] == 'Swamp':
                        deck['Mana']['swamp'] += 1
                    elif board["Side 1"][y]['cmc'] == 'Plains':
                        deck['Mana']['plains'] += 1
                    elif board["Side 1"][y]['cmc'] == 'Forest':
                        deck['Mana']['forest'] += 1
                    else:
                        mana = board["Side 1"][y]['cmc'].split("{").split("}")
                        for x in mana:
                            try:
                                x = int(x)
                            except TypeError:
                                if x.lower() == 'w':
                                    deck['Mana']['plains'] += 1
                                elif x.lower() == 'u':
                                    deck['Mana']['island'] += 1
                                elif x.lower() == 'g':
                                    deck['Mana']['forest'] += 1
                                elif x.lower() == 'r':
                                    deck['Mana']['mountain'] += 1
                                elif x.lower() == 'b':
                                    deck['Mana']['swamp'] += 1
            elif deck['Player Hand'] == 1:
                for i,v in enumerate(board['Side 2']):
                    print(f"{i} | {v}")
                    print()
                tap = input("What cards do you want to tap? ")
                tap = tap.split(',')
                for y in tap:
                    y = int(y)
                    board["Side 2"][y]["Tapped?"] = True
                    if board["Side 2"][y]['cmc'] =='Island':
                        deck['Mana']['island'] += 1
                    elif board["Side 2"][y]['cmc'] == 'Mountain':
                        deck['Mana']['mountain'] += 1
                    elif board["Side 2"][y]['cmc'] == 'Swamp':
                        deck['Mana']['swamp'] += 1
                    elif board["Side 2"][y]['cmc'] == 'Plains':
                        deck['Mana']['plains'] += 1
                    elif board["Side 1"][y]['cmc'] == 'Forest':
                        deck['Mana']['forest'] += 1
                    else:
                        mana = board["Side 2"][y]['cmc'].split("{").split("}")
                        for x in mana:
                            try:
                                x = int(x)
                            except TypeError:
                                if x.lower() == 'w':
                                    deck['Mana']['plains'] += 1
                                elif x.lower() == 'u':
                                    deck['Mana']['island'] += 1
                                elif x.lower() == 'g':
                                    deck['Mana']['forest'] += 1
                                elif x.lower() == 'r':
                                    deck['Mana']['mountain'] += 1
                                elif x.lower() == 'b':
                                    deck['Mana']['swamp'] += 1
            return board

        def place_card(deck,board):
            for i,v in enumerate(deck['Player Hand']):
                print(f" {i} | {v}")
                print()
            place = input("Choose a card to set ")
            # need to run check to see if enough mana has been tapped.
            x = deck["Player Hand"][place]['cmc'].split("{").split("}")

            if deck['Player Turn'] == 0:
                board['Stack'].append({0:deck['Player Hand'][place]})
                board["Side 1"].append(deck['Player Hand'][place])
                if deck['Player Hand'][place]['type_line'][:8] == 'Creature':
                    board['Side 1'].append({'card':deck['Player Hand'][place],'Summoning Sickness?':True,'Tapped?':False})
                else:
                    board['Side 1'].append({'card':deck['Player Hand'][place],'Summoning Sickness?':False,'Tapped?':False})
            elif deck['Player Turn'] == 1:
                board['Stack'].append({1:deck['Player Hand'][place]})
                board['Side 2'].append(deck["Player Hand"][place])
                if deck['Player Hand'][place]['type_line'][:8] == 'Creature':
                    board['Side 2'].append({'card':deck['Player Hand'][place],'Summoning Sickness?':True,'Tapped?':False})
                else:
                    board['Side 2'].append({'card':deck['Player Hand'][place],'Summoning Sickness?':False,'Tapped?':False})
            if deck['Player Hand'][place]['type_line'][:10] == 'Basic Land':
                deck['Land Played?'] = True
            deck["Player Hand"].pop(place)
            cont = True
            while cont:
                continuing = input("Do you want to place another card? ")
                if continuing.lower() == 'yes' or continuing.lower() == 'y':
                    for i,v in enumerate(deck['Player Hand']):
                        print(f" {i} | {v}")
                        print()
                    place = input("Choose a card to set ")
                    if deck['Player Turn'] == 0:
                        board['Stack'].append({0:deck['Player Hand'][place]})
                        board["Side 1"].append(deck['Player Hand'][place])
                    elif deck['Player Turn'] == 1:
                        board['Stack'].append({1:deck['Player Hand'][place]})
                        board['Side 2'].append(deck["Player Hand"][place])
                    if deck['Player Hand'][place]['type_line'][:10] == 'Basic Land':
                        deck['Land Played?'] = True
                    deck["Player Hand"].pop(place)
                elif continuing.lower() == 'no' or continuing.lower() == 'n':
                    cont = False
                else:
                    print("Try Again...")
                return deck,board

        def active_phase(deck,board):
            main_phase = True
            while main_phase:
                PlayerTurn.MainPhase.tap(deck,board)
                PlayerTurn.MainPhase.place_card(deck,board)

                place = input('Do you want to place another card? ')
                if place.lower() == 'yes' or place.lower() == 'y':
                    main_phase = False
                elif place.lower() == 'no' or place.lower() == 'n':
                    continue
                else:
                    print('Try again.')


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
    global playing
    for i in players:
        if i['Life Total'] <= 0:
            playing = False
    return playing

class StartMenu(Screen):
    pass


class DBMenu(Screen):
    pass # while loop for DBMenu

class GameModes(Screen):
    pass # while loop for game modes

class Show():
    pass # 4 separate loops to Show hand, Graveyard, exiled and enemy field

class ChoiceDeck(Screen):
    def selected(self,filename):# Menu to choose or make deck
        try:
            commander_file = os.path.basename(filename[0])
            print("Loading Deck...")
            deck,commander = DeckBuild.deck_manager(commander_file) #not being completed for some reason
            commander = put_in_cz(deck,commander)
            print(player_commander)
            print("Deck Loaded.")
            os.chdir('images')
            print(os.getcwd())
            # Find images for cards store in folder
            # try to create dir if it doesn't exists
            return deck,commander
        except:
            pass
class PvpOne(Screen):
    pass # while loop for PVP ONE V ONE board

class MyGrids(GridLayout):
    def __init__(self,**kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.inside = GridLayout()
        self.inside.cols = 2
        self.cols = 1
        self.inside.add_widget(Label(text='Welcome to Magic the Gathering'))
        self.add_widget(self.inside)
        self.start = Button(text="START",font_size=40)
        self.start.bind(on_press=self.starting)
        self.add_widget(self.start)

    def starting(self,instance):

        start_menu = {'1':"'FIRST TIME DATABASE CREATION'",'2':"'LOAD DATABASE'",'3':"'UPDATE DATABASE'"}
        print('______START MENU______')
        print()
        for k,v in enumerate(start_menu):
            print(f"   {v} | {start_menu[v]}")
            print()
        start = input('Choose a number ')
        if start == '2':
            magic_lib = card_library.load_cards_db()
        else:
            magic_lib = card_library.create_update_cards_db()
        for i in range(8):
            print()
        print("Library Populated")
        print('Items in Library: ' + str(len(magic_lib)))

class MyGrid(Widget):
    pass
class WindowManager(ScreenManager):
    def pressed_create_db(self):
        os.chdir('database/magic_cards')
        print("pressed")
        magic_lib = card_library.create_update_cards_db()

        return magic_lib
    def pressed_load_db(self):
        os.chdir('database/magic_cards')
        print(os.getcwd())
        magic_lib = card_library.load_cards_db()

        return magic_lib

print(os.getcwd())
os.chdir('..')
os.chdir('..')
kv = Builder.load_file('mtg.kv')



class MTGApp(App):
    def build(self):
        return kv


MTGApp().run()

select = input('What mode do you want to play? ')
selecting = True
while selecting:
    if select == '1':
        print('Player One...')
        p1_deck,p1_commander = DeckBuild.deck_manager()
        p1_commander = put_in_cz(p1_deck,p1_commander)
        shuffle(p1_deck)
        p1 = {'Command Zone':p1_commander,'Life Total':30,'Land Played?':False,'Mully Count':0,'Turns Played':0,'Turn_Assign':0,'Mana':{'colorless':0,'island':0,'forest':0,'swamp':0,'mountain':0,'plains':0},'Player Hand':[],'Deck':p1_deck,'Graveyard':{'grave':[],'exiled':[]},}
        p1_mana_total = int(p1['Mana']['colorless'] + p1['Mana']['forest']+ p1['Mana']['island'] + p1['Mana']['swamp'] + p1['Mana']['mountain'] + p1['Mana']['plains'])
        print('Player Two...')
        p2_deck,p2_commander = DeckBuild.deck_manager()
        p2_commander = put_in_cz(p2_deck,p2_commander)
        shuffle(p2_deck)
        p2 = {'Command Zone':p2_commander,'Life Total':30,'Land Played?':False,'Mully Count':0,'Turns Played':0,'Turn_Assign':0,'Mana':{'colorless':0,'island':0,'forest':0,'swamp':0,'mountain':0,'plains':0},'Player Hand': [],'Deck':p2_deck,'Graveyard':{'grave':[],'exiled':[]}}
        p2_mana_total = int(p2['Mana']['colorless'] + p2['Mana']['forest']+ p2['Mana']['island'] + p2['Mana']['swamp'] + p2['Mana']['mountain'] + p2['Mana']['plains'])
        board = {'Side 1': [],'Side 2': [],'Stack':[]}
        for i in range(30):
            print()
        print(str(p1['Command Zone']['name']) + ' V.S. ' + str(p2['Command Zone']['name']))
        for i in range(3):
            print()
        print()
        print()
        print('*********************BOARD*********************')
        print()
        print()
        print(f"{str(p1['Command Zone']['name'])}  |      {board['Side 1']}")
        print()
        print("_______________________________________________")
        print()
        print(f"{str(p2['Command Zone']['name'])}  |      {board['Side 2']}")
        print()
        print()
        print('*********************BOARD*********************')
        print()
        print("_______________________________________________")
        print()
        print(f"Player One Life: {p1['Life Total']}     |     Player Two Life: {p2['Life Total']}")

        playing = True
        while playing:
            players = [p1,p2]
            for i in players:
                if i['Turn_Assign'] == 0:
                    PlayerTurn.Draw.draw_seven(i)
                    print(i['Player Hand'])
                    print()
                    option1 = input("Do you want to mully? ")
                    if option1.lower() == "yes" or option1.lower() == "y":
                        PlayerTurn.Draw.mully(i)
                        shuffle(i['Deck'])
                        print(i['Player Hand'], len(i['Player Hand']))
                        option1 = input("Are you satisfied with your mully? ")
                        if option1.lower() == "no" or option1.lower() == "n":
                            PlayerTurn.Draw.mully(i)
                            shuffle(i['Deck'])
                            for x in i['Player Hand']:
                                print()
                                print(x)
                            option1 = input("Are you satisfied with your mully? ")
                            if option1.lower() == "no" or option1.lower() == "n":
                                print("Okay Last Super Mully")
                                PlayerTurn.Draw.mully(i)
                                shuffle(i['Deck'])
                                for x in i['Player Hand']:
                                    print()
                                    print(x)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                    print(i["Player Hand"])
                    if i["Mully Count"] > 0:
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
                    else:
                        pass
                    print("First Player has finished their turn")
                    i['Turns Played'] += 1
                    print()
                    print()
                    print('*********************BOARD*********************')
                    print()
                    print()
                    print(f"{str(p1['Command Zone']['name'])}  |      {board['Side 1']}")
                    print()
                    print("_______________________________________________")
                    print()
                    print(f"{str(p2['Command Zone']['name'])}  |      {board['Side 2']}")
                    print()
                    print()
                    print('*********************BOARD*********************')
                    print()
                    print("_______________________________________________")
                    print()
                    print(f"Player One Life: {p1['Life Total']}     |     Player Two Life: {p2['Life Total']}")
                    # player 1 goes through game phases

                check_winner(players)
                if i['Turn_Assign'] == 1:
                    pass
                    PlayerTurn.Draw.draw_seven(i)
                    print(i['Player Hand'],len(i['Player Hand']))
                    print()
                    option1 = input("Do you want to mully? ")
                    if option1.lower() == "yes" or option1.lower() == "y":
                        PlayerTurn.Draw.mully(i)
                        shuffle(i['Deck'])
                        print(i['Player Hand'], len(i['Player Hand']))
                        option1 = input("Are you satisfied with your mully? ")
                        if option1.lower() == "no" or option1.lower() == "n":
                            PlayerTurn.Draw.mully(i)
                            shuffle(i['Deck'])
                            for x in i['Player Hand']:
                                print()
                                print(x)
                            option1 = input("Are you satisfied with your mully? ")
                            if option1.lower() == "no" or option1.lower() == "n":
                                print("Okay Last Super Mully")
                                PlayerTurn.Draw.mully(i)
                                shuffle(i['Deck'])
                                for x in i['Player Hand']:
                                    print()
                                    print(x)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                    print(i["Player Hand"])
                    print(f"Second Player has finished their turn")
                    i['Turns Played'] += 1
                    print()
                    print()
                    print('*********************BOARD*********************')
                    print()
                    print()
                    print(f"{str(p1['Command Zone']['name'])}  |      {board['Side 1']}")
                    print()
                    print("_______________________________________________")
                    print()
                    print(f"{str(p2['Command Zone']['name'])}  |      {board['Side 2']}")
                    print()
                    print()
                    print('*********************BOARD*********************')
                    print()
                    print("_______________________________________________")
                    print()
                    print(f"Player One Life: {p1['Life Total']}     |     Player Two Life: {p2['Life Total']}")
                    # Player 2 goes through game phases
                check_winner(players)
            playing = False

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
