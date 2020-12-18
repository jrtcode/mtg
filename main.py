import os
import sqlite3 as sql
from database.magic_cards import card_library
from database.deck_builder import deck_build

# print(os.getcwd())
# os.chdir('database/')
# os.chdir('magic_cards/')
#
# conn = sql.connect('mtg-cards.db')
# cur = conn.cursor()
# cur.execute("SELECT * FROM magic_cards")
# cards_db = cur.fetchall()

magic_lib = card_library.cards_db()


deck = deck_build.deck_manager()

print(deck)
