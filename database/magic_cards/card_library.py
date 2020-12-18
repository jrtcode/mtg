import requests
from bs4 import BeautifulSoup as bs
import os
import sqlite3 as sql


def cards_db():
    if os.path.exists('mtg-cards.db') == False:
        conn = sql.connect('mtg-cards.db')
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE magic_cards(
                        card_name text,
                        converted_mana_cost text,
                        card_type_line text,
                        card_stats text,
                        card_text_box text,
                        card_name_back text,
                        card_type_line_back text,
                        card_stats_back text,
                        card_text_box_back text)""")
        except sql.OperationalError:
            pass
            # This can be where updating the database could go?


        # x = 198
        path = 'images/'
        try:
            os.mkdir(os.path.join(os.getcwd(),path))
        except:
            pass

        card_database = {}

        for x in range(1,1021):
            url = "https://scryfall.com/search?as=full&order=name&page="
            page = requests.get(url+str(x)+"&q=color%3C%3DWUBRG+legal%3Acommander+lang%3Aen&unique=cards")

            soup = bs(page.content,'html.parser')

            cards = soup.find_all(class_='card-profile')

            for card in cards:
                img = card.find('img')['src']
                try:
                    img_back = card.find('div',class_='card-image-back').img['src']
                    name_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                    type_line_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                    type_line_back = type_line_back.replace('\n          ',' ')
                    stats_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                    text_box_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                    text_box_back = text_box_back.replace('\n',' ')
                except AttributeError:
                    img_back = ''
                name = card.find('h1', class_='card-text-title').text.strip()
                try:
                    cmc = card.find('span',class_='card-text-mana-cost').text.strip()
                except AttributeError:
                    cmc = name.split()[-1]
                name = name.split('{',1)
                name = name[0]
                name = name.replace('\n           ','')
                if name[-1] == ' ':
                    name = name[:-1]
                type_line = card.find('p',class_='card-text-type-line').text.strip()
                try:
                    text_box = card.find('div',class_='card-text-oracle').text.strip()
                    text_box = text_box.replace('\n',' ')
                except AttributeError:
                    try:
                        text_box = card.find('div',class_='card-text-flavor').text.strip()
                        text_box = text_box.replace('\n',' ')
                    except AttributeError:
                        text_box = 'N/A'
                try:
                    stats = card.find('div',class_='card-text-stats').text.strip()
                except AttributeError:
                    stats = 'N/A'
                magic_card= {
                    'name':name,
                    'cmc':cmc,
                    'type_line':type_line,
                    'text_box':text_box,
                    'card_stats':stats
                }
                if len(img_back) > 0:
                    c.execute("INSERT INTO magic_cards VALUES (?,?,?,?,?,?,?,?,?)",[magic_card['name'],magic_card['cmc'],magic_card['type_line'],magic_card['card_stats'],magic_card['text_box'],name_back,type_line_back,stats_back,text_box_back,])
                else:
                    c.execute("INSERT INTO magic_cards VALUES (?,?,?,?,?,?,?,?,?)",[magic_card['name'],magic_card['cmc'],magic_card['type_line'],magic_card['card_stats'],magic_card['text_box'],'N/B','N/B','N/B','N/B',])
                print(name.replace('\n           ','')+' added to database.')
                os.chdir(os.path.join(os.getcwd(),path))
                img_file = open(name.replace(' ','-').replace(',','').replace('"','')+".jpg",'wb')
                im = requests.get(img)
                img_file.write(im.content)
                img_file.close()
                print('Saving ' + name.replace('\n           ','') + ' image')
                try:
                    if len(img_back) > 0:
                        img_file = open(name.replace(' ','-').replace(',','').replace('"','')+"back.jpg",'wb')
                        im = requests.get(img_back)
                        img_file.write(im.content)
                        img_file.close()
                        print('Saving ' + name.replace('\n           ','') + 'back image')
                        img_back = None
                except:
                    pass
                os.chdir("..")
                card_database[str(name)] = magic_card
            print(str(len(card_database)) + " total cards added. Completed page "+ str(x) + "...")
            # print(card_database)
        conn.commit()
        conn.close()
        print('Finished.')
        print('Cards Added to Database: '+ str(len(card_database)))
    else:
        print("Would you like to add more cards to your card database?")
        print("This can take a while, as there are a lot of cards to check for any new additions...")
        print("Are you sure you want to try to update?")
        answer = input("Yes or No?")
        if answer.lower() == 'yes':
            os.chdir('database/magic_cards')
            conn2 = sql.connect('mtg-cards.db')
            cur2 = conn2.cursor()
            cur2.execute("""CREATE TABLE updated_magic_cards(
                        card_name text,
                        converted_mana_cost text,
                        card_type_line text,
                        card_stats text,
                        card_text_box text,
                        card_name_back text,
                        card_type_line_back text,
                        card_stats_back text,
                        card_text_box_back text)""")
            # x = 317
            path = 'images/'
            try:
                os.mkdir(os.path.join(os.getcwd(),path))
            except:
                pass

            card_database = {}
            for x in range(1,1021):
                url = "https://scryfall.com/search?as=full&order=name&page="
                page = requests.get(url+str(x)+"&q=color%3C%3DWUBRG+legal%3Acommander+lang%3Aen&unique=cards")

                soup = bs(page.content,'html.parser')

                cards = soup.find_all(class_='card-profile')

                for card in cards:
                    img = card.find('img')['src']
                    try:
                        img_back = card.find('div',class_='card-image-back').img['src']
                        name_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                        type_line_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                        type_line_back = type_line_back.replace('\n          ',' ')
                        stats_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                        text_box_back = card.find('h1',class_='card-text-title').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                        text_box_back = text_box_back.replace('\n',' ')
                    except AttributeError:
                        img_back = ''
                    name = card.find('h1', class_='card-text-title').text.strip()
                    try:
                        cmc = card.find('span',class_='card-text-mana-cost').text.strip()
                    except AttributeError:
                        cmc = name.split()[-1]
                    name = name.split('{',1)
                    name = name[0]
                    name = name.replace('\n           ','')
                    if name[-1] == ' ':
                        name = name[:-1]
                    type_line = card.find('p',class_='card-text-type-line').text.strip()
                    try:
                        text_box = card.find('div',class_='card-text-oracle').text.strip()
                        text_box = text_box.replace('\n',' ')
                    except AttributeError:
                        try:
                            text_box = card.find('div',class_='card-text-flavor').text.strip()
                            text_box = text_box.replace('\n',' ')
                        except AttributeError:
                            text_box = 'N/A'
                    try:
                        stats = card.find('div',class_='card-text-stats').text.strip()
                    except AttributeError:
                        stats = 'N/A'
                    magic_card= {
                        'name':name,
                        'cmc':cmc,
                        'type_line':type_line,
                        'text_box':text_box,
                        'card_stats':stats
                    }
                    if len(img_back) > 0:
                        cur2.execute("INSERT INTO updated_magic_cards VALUES (?,?,?,?,?,?,?,?,?)",[magic_card['name'],magic_card['cmc'],magic_card['type_line'],magic_card['card_stats'],magic_card['text_box'],name_back,type_line_back,stats_back,text_box_back,])
                    else:
                        cur2.execute("INSERT INTO updated_magic_cards VALUES (?,?,?,?,?,?,?,?,?)",[magic_card['name'],magic_card['cmc'],magic_card['type_line'],magic_card['card_stats'],magic_card['text_box'],'N/B','N/B','N/B','N/B',])
                    print(name.replace('\n           ','')+' added to database.')
                    os.chdir(os.path.join(os.getcwd(),path))
                    img_file = open(name.replace(' ','-').replace(',','').replace('"','')+".jpg",'wb')
                    im = requests.get(img)
                    img_file.write(im.content)
                    img_file.close()
                    print('Saving ' + name.replace('\n           ','') + ' image')
                    try:
                        if len(img_back) > 0:
                            img_file = open(name.replace(' ','-').replace(',','').replace('"','')+"back.jpg",'wb')
                            im = requests.get(img_back)
                            img_file.write(im.content)
                            img_file.close()
                            print('Saving ' + name.replace('\n           ','') + 'back image')
                            img_back = None
                    except:
                        pass
                    os.chdir("..")
                    card_database[str(name)] = magic_card
                print(str(len(card_database)) + " total cards added. Completed page "+ str(x) + "...")
            cur2.execute("""SELECT * FROM magic_cards
                            UNION
                            SELECT * FROM updated_magic_cards""")
            cur2.execute("""DROP TABLE updated_magic_cards""")
            conn2.commit()
            rows = cur2.fetchall()
            magic_cards = []
            for row in rows:
                magic_cards.append(row)
            print(len(magic_cards))
            conn2.close()
            print('Finished.')
            print('Cards Added to Database: '+ str(len(card_database)))
        elif answer.lower() =='no':
            conn = sql.connect('mtg-cards.db')
            cur = conn.cursor()
            cur.execute("""SELECT * FROM magic_cards""")
            rows = cur.fetchall()
            magic_cards = []
            for row in rows:
                magic_cards.append(row)
                # print(row)
                # print()
                # print()
            print('Magic cards added to list from database.')
            return magic_cards
        # print(card_database)


if __name__ == "__main__":
    cards_db()
