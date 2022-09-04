import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")

ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")

values = {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8,
          "Nine":9, "Ten":10, "Jack":10, "Queen":10, "King":10, "Ace":11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck_cards = []
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.deck_cards.append(new_card)

    def __str__(self):
        return f"{self.deck_cards}"

    def shuffle(self):
        random.shuffle(self.deck_cards)

    def deal(self):
        return self.deck_cards.pop()

class Hand:
    def __init__(self):
        self.hand_cards = []
        self.hand_value = 0 #start with zero value
        self.aces = 0 #ace counter

    def add_card(self, card):
        self.hand_cards.append(card)
        self.hand_value += values[card.rank] #ths sugekrimenhs kartas to rank
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.hand_value > 21 and self.aces:
            self.hand_value -= 10
            self.aces -= 1

class Chips:
    def __init__(self, chips):
        self.total = chips
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_a_bet(chips):
    while True:
        print(f"you have a total of {chips.total} chips")
        try:
            chips.bet = int(input("Give me your bet: "))
        except ValueError:
            print("Your bet must be an integer number")
        else:
            if chips.bet > chips.total:
                print("You dont have enough chips for this betting")
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stop(deck, hand):
    global playing

    while True:
        answer = input("Do you want to hit or stop? press h for hit, s for stop: ")
        if answer[0] == "h":
            hit(deck, hand)
        elif answer[0] == "s":
            print("Player Stands")
            playing = False
        else:
            print("Please try again")
            continue
        break

def show_some(player, dealer):
    print("\nDealers hand:")
    print("<<card hidden>> ")
    print(dealer.hand_cards[0])
    print("\nPlayer hand: ", *player.hand_cards, sep="\n")

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.hand_cards)
    print("Dealer's Hand =", dealer.hand_value)
    print("\n Player hand: ", *player.hand_cards, sep="\n")
    print("Player's Hand =", player.hand_value)

def player_busts(player, dealer, chips):
    print("Player busted")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("dealer busted")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("dealer wins")
    chips.lose_bet()

def push():
    print("we have a tie")

new_chips = int(input("with how many chips are you going to play? "))
player_1_chips = Chips(new_chips)

while True:
    print("We are playing Black Jack, Get as close as possible to 21 without getting busted\n"
          "Dealer hits until reaches 17. Aces count as 11 or 1")
    new_deck = Deck()
    new_deck.shuffle()

    player_1 = Hand()
    dealer = Hand()

    for i in range(2):
        player_1.add_card(new_deck.deal())
        dealer.add_card(new_deck.deal())

    take_a_bet(player_1_chips)

    show_some(player_1, dealer)

    while playing:
        hit_or_stop(new_deck, player_1)

        show_some(player_1, dealer)

        if player_1.hand_value > 21:
            #player_busts(player_1, dealer, player_1_chips)
            break

    if player_1.hand_value <= 21:
        while dealer.hand_value <= 17:
            hit(new_deck, dealer)

    show_all(player_1, dealer)

    if dealer.hand_value > 21:
        player_wins(player_1, dealer, player_1_chips)
    elif player_1.hand_value > 21:
        dealer_wins(player_1, dealer, player_1_chips)
    elif player_1.hand_value > dealer.hand_value:
        player_wins(player_1, dealer, player_1_chips)
    elif dealer.hand_value > player_1.hand_value:
        dealer_wins(player_1, dealer, player_1_chips)
    else:
        push()

    if player_1_chips.total == 0:
        print("You have run out of chips, I am sorry")

        break
    new_game = input("Do you want to play a new round, press Y for yes or N for no: ")

    if new_game[0].lower() == "y":
        playing = True
    else:
        break