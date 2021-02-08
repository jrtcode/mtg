# Magic the Gathering
W.I.P. version 0.1
# Create Magic Card Library
Run card_library.py first to create .db file. This will take a while since there are over 20,000 cards to grab from Scryfall.com
It will save all the card images in the magic_cards/images folder under database.
Once it has created the library you must create a deck to save

# Create a deck 
There isn't too much of a limit when it comes to making your deck. Run the deck_build.py file and it will ask what card is your commander. Remember how you type this name as it will be saved as that .db to user_decks for later use. DO NOT USE SPECIAL CHARACTERS :",'*&%$#@!~()./?[]{}

# Update
W.I.P. version 0.2  (Current) 
# Create Magic Card Library
running the main.py should download the cards just run main.py if this doesn't work
Run card_library.py to create .db file. YOU NEED THE "mtg-cards.db" FILE TO START TO THE GAME.
This download will take a while since there are over 20,000 cards to grab from Scryfall.com
It will save all the card images in the magic_cards/images folder under database.
Once it has created the library you must create a deck to save.
I uploaded a couple of my decks for testing which can be found in the user_decks folder.
You can alternatively load these test decks.

# Creating a deck 
There isn't too much of a limit when it comes to making your deck, the game style is Commander. So 1 Commander, 99 other cards no duplicates unless its a basic land.  Run the main.py file and it will bring up a menu. Choose option 4 'Create a Deck'. It will then ask what card is your commander. Remember how you type this name as it will be saved as that .db to user_decks for later use. DO NOT USE SPECIAL CHARACTERS :",'*&%$#@!~()./?[]{}
When adding cards to your deck the prompt will first ask you to type the name of the card you want to add.
ADD YOUR COMMANDER FIRST, Then the rest of your cards
TYPE CARD NAMES AS YOU SEE THEM ON THE CARD... CAPS DON'T MATTER BUT PUNCUATIONS DO. (COMMAS AND DASHES)
Once you enter the name and press 
then your Camera will turn on prompting you to press esc. 
Here you are suppose to take a picture of your card and with Key point detection it will add the corresponding card, provided enough keypoints are found.  18 keypoints or better for a good match.

# Menu Options
After the download of "mtg-cards.db" if you start main.py script
you will be asked "if you want to update" choose no.
then choose game mode. Only game mode 1 has some code made Game modes are a work in progress
