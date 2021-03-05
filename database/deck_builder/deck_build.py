import os
import sqlite3 as sql
import numpy as np
import matplotlib.pyplot as plt
import cv2
import re

# print(os.getcwd())

dir = os.listdir(os.getcwd())

if 'deck_build.py' in dir:
    os.chdir('..')
    os.chdir('..')
    print('found deck_build.py')
# print(dir)
path = 'magic_cards/'
# print(os.getcwd())
os.chdir('database/')
# print(os.getcwd(),'current')
os.chdir(path)

conn = sql.connect('mtg-cards.db')
cur = conn.cursor()
cur.execute("SELECT * FROM magic_cards")
cards_db = cur.fetchall()

conn.close()
#MUST RUN CARD_LIBRARY
class DeckBuild():
    def card_library():
        magic_cards = {}
        for card in cards_db:
            magic_card = {
                'name': card[0],
                'cmc':card[1],
                'type_line':card[2],
                'stats':card[3],
                'textbox':card[4],
                'name_back':card[5],
                'type_line_back':card[6],
                'stats_back':card[7],
                'textbox_back':card[8]
            }
            magic_cards[card[0]] = magic_card
            # print(card)

        return magic_cards

    def countOccurance(deck,card_name):
        count = 0
        for ele in deck:
            if len(ele) == 0:
                deck.remove(ele)
            if ele['name'] == card_name:
                count = count + 1
        return count

    def deck_build():
        building = True
        deck = []
        library = {k.lower(): v for k,v in DeckBuild.card_library().items()}
        print(os.path.basename(os.getcwd()))
        if os.path.basename(os.getcwd()) == 'deck_builder':
            os.chdir('..')
            os.chdir('magic_cards/')
            os.chdir('images/')
        commander = input('What is the name of your Commander for this deck, as you see it on the card? ')
        while building:
            addition = input("What's the name of the card you want to add? ")
            if addition.lower() in library.keys():
                card = library[addition.lower()]
                img_name = card['name'].replace(' ','-').replace(',','').replace('"','') +'.png'
                found_img = [x for x in os.listdir() if img_name in x]
                found_img = found_img[0]
                found_img = cv2.imread(found_img,0)

                if card['name_back'] != 'N/B':
                    back_img = card['name'].replace(' ','-').replace(',','').replace('"','')+"back.png"
                    found_img2 = [x for x in os.listdir() if back_img in x]
                    found_img2 = found_img2[0]
                    found_img2 = cv2.imread(found_img2)

                    print("Card's transform found!")

                if cv2.waitKey(1) & 0xFF == 27:
                    cv2.destroyAllWindows()

                cap = cv2.VideoCapture(0)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                while cap.isOpened():
                    ret,frame = cap.read()
                    cv2.putText(frame,f"PRESS ESC, TAKE SNAPSHOT OF {card['name']}",(75,50),cv2.FONT_HERSHEY_COMPLEX,.5,(0,255,0),2)
                    cv2.imshow('Take a Snapshot',frame) #display the captured image
                    if cv2.waitKey(1) & 0xFF == 27: #save on pressing 'y'
                        print(os.getcwd())
                        os.chdir('..')
                        os.chdir('user_img')
                        cv2.imwrite(os.path.join(os.getcwd(),img_name),frame)
                        cv2.destroyAllWindows()
                        break
                print()
                print()
                user_img = cv2.imread(img_name,0)
                cap.release()
                # AREA FOR OPENCV TO COMPARE CARD
                orb = cv2.ORB_create(nfeatures=2000)

                kp1,des1 = orb.detectAndCompute(found_img,None)
                kp2,des2 = orb.detectAndCompute(user_img,None)

                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1,des2,k=2)

                good = []

                for m,n in matches:
                    if m.distance < 0.75*n.distance:
                        good.append([m])
                m_img = cv2.drawMatchesKnn(user_img,kp1,found_img,kp2,good,None,flags=2)

                if addition.lower() == 'mountain':
                    if len(good) >= 18:
                        print(len(good))
                        print('CARD MATCHED!!!')
                        print(card)
                        deck.append(card)
                        os.remove(img_name)
                    else:
                        print(len(good))
                        print("THE CARD YOU TOOK A PICTURE OF DIDN'T MATCH THE CARD YOU TYPED")
                        print()
                        print("Try Again.")
                        os.remove(img_name)
                elif addition.lower() == 'plains':
                    if len(good) >= 16:
                        print(len(good))
                        print('CARD MATCHED!!!')
                        print(card)
                        deck.append(card)
                        os.remove(img_name)
                    else:
                        print(len(good))
                        print("THE CARD YOU TOOK A PICTURE OF DIDN'T MATCH THE CARD YOU TYPED")
                        print()
                        print("Try Again.")
                        os.remove(img_name)
                else:
                    if len(good) >= 18:
                        print(len(good))
                        print('CARD MATCHED!!!')
                        print(card)
                        deck.append(card)
                        os.remove(img_name)
                    else:
                        print(len(good))
                        print("THE CARD YOU TOOK A PICTURE OF DIDN'T MATCH THE CARD YOU TYPED")
                        print()
                        print("Try Again.")
                        os.remove(img_name)
            elif addition.lower() + ' ' in library:
                card = library[addition.lower()]
                img_name = card['name'].replace(' ','-').replace(',','').replace('"','') +'.png'
                found_img = [x for x in os.listdir() if img_name in x]
                found_img = found_img[0]
                found_img = cv2.imread(found_img,0)

                if card['name_back'] != 'N/B':
                    back_img = card['name'].replace(' ','-').replace(',','').replace('"','')+"back.png"
                    found_img2 = [x for x in os.listdir() if back_img in x]
                    found_img2 = found_img2[0]
                    found_img2 = cv2.imread(found_img2)

                    print("Card's transform found!")

                if cv2.waitKey(1) & 0xFF == 27:
                    cv2.destroyAllWindows()

                cap = cv2.VideoCapture(0)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                while cap.isOpened():
                    ret,frame = cap.read()
                    cv2.putText(frame,f"PRESS ESC, TAKE SNAPSHOT OF {card['name']}",(75,50),cv2.FONT_HERSHEY_COMPLEX,.5,(0,255,0),2)
                    cv2.imshow('Take a Snapshot',frame) #display the captured image
                    if cv2.waitKey(1) & 0xFF == 27: #save on pressing 'y'
                        print(os.getcwd())
                        os.chdir('..')
                        os.chdir('user_img')
                        cv2.imwrite(os.path.join(os.getcwd(),img_name),frame)
                        cv2.destroyAllWindows()
                        break
                print(os.getcwd())
                print()
                print()
                user_img = cv2.imread(img_name,0)
                cap.release()
                # AREA FOR OPENCV TO COMPARE CARD
                orb = cv2.ORB_create(nfeatures=2000)

                kp1,des1 = orb.detectAndCompute(found_img,None)
                kp2,des2 = orb.detectAndCompute(user_img,None)

                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1,des2,k=2)

                good = []

                for m,n in matches:
                    if m.distance < 0.75*n.distance:
                        good.append([m])
                m_img = cv2.drawMatchesKnn(user_img,kp1,found_img,kp2,good,None,flags=2)
                if len(good) >= 19:
                    print(len(good))
                    print('CARD MATCHED!!!')
                    print(card)
                    deck.append(card)
                    os.remove(img_name)
                else:
                    print(len(good))
                    print("THE CARD YOU TOOK A PICTURE OF DIDN'T MATCH THE CARD YOU TYPED")
                    print()
                    print("Try Again.")
                    os.remove(img_name)
            else:
                print("Card isn't in Library...")
                card = 'N/A'
            if card == 'N/A':
                pass
            else:
                count = DeckBuild.countOccurance(deck,card['name'])
                if count >= 2:
                    if card['type_line'][:10] == 'Basic Land':
                        pass
                    else:
                        print('Sorry you can only have duplicate basic lands in commander format.')
                        print(card['type_line'][:10])
                        deck = deck[:-1]
                        print("Don't worry the card was removed, continue with adding more cards.")
                print("Cards in Deck: "+ str(len(deck)))
                if len(deck) <= 100:
                    if len(deck) == 100:
                        print('You have reached the maximum amount of cards you can add to your deck.')
                        building = False
                        break
                    else:
                        continuing = True
                        while continuing:
                            cont = input('Do you want to add another card? ')
                            if cont.lower() == 'yes':
                                os.chdir('..')
                                os.chdir('images/')
                                continuing = False
                            elif cont.lower() == 'y':
                                os.chdir('..')
                                os.chdir('images/')
                                continuing = False
                            elif cont.lower() == 'no':
                                os.chdir('..')
                                os.chdir('..')
                                os.chdir('deck_builder/')
                                os.chdir('user_decks/')
                                building = False
                                continuing = False
                            elif cont.lower() == 'n':
                                os.chdir('..')
                                os.chdir('..')
                                os.chdir('deck_builder/')
                                os.chdir('user_decks/')
                                building = False
                                continuing = False
                            else:
                                print("TRY AGAIN, I DIDN'T CATCH THAT.")
                if len(deck) <= 100:
                    print(f"Added to '{card['name']}' your '{commander}' deck...")

        return deck,commander

    def deck_manager(commander):
        # print(os.getcwd())
        if os.path.basename(os.getcwd()) == 'images':
            os.chdir('..')
        building = True
        deck = []
        library = {k.lower(): v for k,v in DeckBuild.card_library().items()}
        # commander = input('What is the name of the commander in your deck? ')

        os.chdir('images/')
        os.chdir('..')
        os.chdir('..')
        os.chdir('deck_builder/')
        os.chdir('user_decks/')


        conn = sql.connect(commander)
        cur = conn.cursor()

        try:
            cur.execute("""CREATE TABLE magic_deck(
                        card_name text,
                        converted_mana_cost text,
                        card_type_line text,
                        card_stats text,
                        card_text_box text,
                        card_name_back text,
                        card_type_line_back text,
                        card_stats_back text,
                        card_text_box_back text)""")
            os.chdir('..')
            os.chdir('..')
            os.chdir('magic_cards/')
            os.chdir('images/')
            deck,commander = DeckBuild.deck_build()
            print(deck)
            for card in deck:
                cur.execute("INSERT INTO magic_deck VALUES (?,?,?,?,?,?,?,?,?)",[card['name'],card['cmc'],card['type_line'],card['stats'],card['textbox'],card['name_back'],card['type_line_back'],card['stats_back'],card['textbox_back'],])
                print(f"SAVED {card['name']} to database...")
            print('DONE.')
            print('DECK SAVED.')
            print(f"YOU CAN LOAD IT BY TYPING IN '{commander}' INTO THE PROMPT WHEN ASKED WHO IS YOUR COMMANDER.")
        except sql.OperationalError:
            cur.execute("SELECT * FROM magic_deck")
            cards = cur.fetchall()
            for card in cards:
                magic_card = {
                    'name': card[0],
                    'cmc':card[1],
                    'type_line':card[2],
                    'stats':card[3],
                    'textbox':card[4],
                    'name_back':card[5],
                    'type_line_back':card[6],
                    'stats_back':card[7],
                    'textbox_back':card[8]
                }
                deck.append(magic_card)
                DeckBuild.countOccurance(deck,magic_card)
            conn.close()
            os.remove(f'{commander}.db')
            print(deck, 'After removal of database')
            conn = sql.connect(f'{commander}.db')
            cur = conn.cursor()
            cur.execute("""CREATE TABLE magic_deck(
                        card_name text,
                        converted_mana_cost text,
                        card_type_line text,
                        card_stats text,
                        card_text_box text,
                        card_name_back text,
                        card_type_line_back text,
                        card_stats_back text,
                        card_text_box_back text)""")
            os.chdir('..')
            os.chdir('..')
            os.chdir('magic_cards/')
            os.chdir('images/')
            if len(deck) < 100:
                print(deck)
                DeckBuild.deck_build()
            print(deck)
            for card in deck:
                cur.execute("INSERT INTO magic_deck VALUES (?,?,?,?,?,?,?,?,?)",[card['name'],card['cmc'],card['type_line'],card['stats'],card['textbox'],card['name_back'],card['type_line_back'],card['stats_back'],card['textbox_back'],])
                print(f"SAVED {card['name']} to database...")
            print('DONE.')
            print('DECK SAVED.')
            print(f'YOU CAN LOAD IT BY TYPING IN {commander} INTO THE PROMPT WHEN ASKED WHO IS YOUR COMMANDER.')
        conn.commit()
        conn.close()
        return deck,commander





if __name__ == "__main__":
    print(os.getcwd())
    path = 'magic_cards/'
    os.chdir('..')
    print(os.getcwd())
    os.chdir(path)
    conn = sql.connect('mtg-cards.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM magic_cards")
    cards_db = cur.fetchall()
    print(os.getcwd())
    os.chdir('..')
    os.chdir('deck_builder/')
    DeckBuild.card_library()
    DeckBuild.deck_build()
