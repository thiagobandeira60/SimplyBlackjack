import random

# The first step is to actually create the deck. The deck must contain 52 cards, 13 for every suit.
# The values will be attached to each card later

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

# The class Card is defined below.
# This class attaches the ranks to the suits, printing 'two of diamonds' for instance.

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

# The Deck class is the one that actually builds the deck itself.
# It makes every possible combination of suits and ranks
# and appends them to the list self.deck.
# Additionally, it shuffles the deck, making it random every time the game is played.

class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

# The class Hand is built to calculate the value of each card. It also defines the value
# of ace depending on the situation. Ace starts being 11 (as showed on value's dictionary, at the beggining)
# However, it can be 1 depending on what you have on your hand.
# The add_card function adds cards to each player, but if it is an ace, it counts.
# the adjust_for_ace function changes the value of an ace depending on what the player has. It also adjusts
# the number of aces.

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces
    # If total value > 21 and I still have an ace
    # Then chnge my ace to be a 1 instead of 11
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# The Chips class keeps track of the player's starting chips, bets, and ongoing winnings.

class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Now that the classes were created, some functions are defined in order to build the game's logic.

# The take_bet function makes sure the player has enough chips to bet.

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except:
            print('Sorry, please provide an integer')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you do not have enough chips! You have: {chips.total}')
            else:
                break
# The hit function is responsible for allowing players to take hits until they bust.
# It's also necessary to to check the value of an ace (if it's 1 or 11).

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# the hit_or_stand function is responsible for asking the players if they want to hit or stand.
# In case they don't type h or s, they will be prompt to try again.

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

# The show_some and show_all functions represent the scenario of the player and the
# dealer turns. Each one receives two cards, but ons of the dealer's cards is hidden.

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

# The following functions show the various possible scenarios, where the player or the dealer
# wins. It also adds or subtracts the chips depending on the result.

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("The Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("The Dealer wins!")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

# The game starts!

while True:
    print('Welcome to BlackJack! See if you can get 21, or as close as 21 as you can!\nAces count as 1 or 11.')

    # The deck is created and shuffled. Each player receives 2 cards.
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # The player's chips is set up
    player_chips = Chips()  # remember the default value is 100

    # The player is prompt to take a bet
    take_bet(player_chips)

    # Cards are shown
    show_some(player_hand,dealer_hand)

    while playing:

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Test for different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)

    # Inform Player of their chips total
    print("\nThe player went down to {} chips".format(player_chips.total))

    # Ask to play again
    new_game = input("Would you like to keep playing? Enter 'y' or 'n' ")
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("See you later!")
        break
