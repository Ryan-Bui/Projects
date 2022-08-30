class base:
    SILENT=6
    DEBUG=1
    INFO=2
    WARNING=3
    ERROR=4
    CRITICAL=5
    
    def __init__(self,level=0):
        self.level=level
        
    def message(self,level,*args):
        if level >= self.level:
            print(*args)
        

class Card(base):
    __suits = ["Clubs", "Diamonds", "Hearts", "Spades", "ShuffleCard"]
    __values = list(range(2,11)) + [ "Jack", "Queen", "King", "Ace"]

    def __init__(self,suit,value=None):
        base.__init__(self)
        self.__suit = suit if suit in self.__suits else None
        self.__value = value if value in self.__values else None
        
        if self.__suit is None:
            self.message(self.ERROR, "Error, bad suit:",suit)

        if self.__value is None and self.__suit != "ShuffleCard":
            self.message(self.ERROR, "Error, bad value:",value)

    def value(self):
        return self.__value
    
    def suit(self):
        return self.__suit
    
    def numerical_value(self):
        # Special Handling of aces
        if self.__value == "Ace":
            return 1
        elif self.__value in [ "Jack", "Queen", "King"]:
            return 10
        elif self.__value == None:
            return 0
        else:
            return self.__value
############################################################ code that I added in starts      
    def same_suit_as(self,card):
        if self.__suit == card.__suit:
            return True
        else:
            return False
    def same_value_as(self,card):
        if self.__value == card.__value:
            return True
        else:
            return False
    def same_numerical_value_as(self,card):
        if self.numerical_value() == card.numerical_value():
            return True
        else:
            return False
    def greater_numerical_value_as(self,card):
        if self.numerical_value() < card.numerical_value():
            return True
        else:
            return False

    def __eq__(self,card):
        if self.same_suit_as(card) and self.same_value_as(card) and self.same_numerical_value_as(card):
            return True
        else:
            return False
############################################################ code that I added in ends       
        
    def shuffle_card(self):
        return self.__suit == "ShuffleCard"

    def __str__(self):
        if self.shuffle_card():
            return "Shuffle Card"
        else:
            return str(self.__value) + " of " + self.__suit

    __repr__ = __str__
    
import random
############################################################ code that I added in starts      
class CardFilterFunction:
    def __init__(self):
        pass
    def __call__(self,card):
        raise NotImplementedError

class CheckSuit(CardFilterFunction):
    def __init__(self,suit):
        super().__init__()
        self.__suit = suit
        
    def __call__(self,card):
        if self.__suit == card.suit():
            return True
        else:
            return False
        

class CheckValue(CardFilterFunction):
    def __init__(self,val):
        super().__init__()
        self.__val = val
        
    def __call__(self,card):
        if self.__val == card.value():
            return True
        else:
            return False

class CheckNumericalValue(CardFilterFunction):
    def __init__(self,num_val):
        super().__init__()
        self.__num_val = num_val
    def __call__(self,card):
        if self.__num_val == card.numerical_value():
            return True
        else:
            return False
        
class CheckGrNumericalValue(CardFilterFunction):
    def __init__(self,num_val):
        super().__init__()
        self.__num_val = num_val
        
    def __call__(self,card):
        #print(card.numerical_value())
        if self.__num_val <= card.numerical_value():
            return True
        else:
            return False

############################################################ code that I added in ends        
class Deck(base):
    __suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    __values = list(range(2,11)) + [ "Jack", "Queen", "King", "Ace"]

    def __init__(self,n_decks=6):
        base.__init__(self)
        self.__n_decks=n_decks
        
        self.__cards = list()
        
        for _ in range(self.__n_decks):
            self.__cards.extend(self.__make_deck())            
            
        # TODO: Add logic to appropriately place shufflecard
        self.__cards.append(Card("ShuffleCard"))
        
    def __make_deck(self):
        deck=list()
        for suit in self.__suits:
            for value in self.__values:
                deck.append(Card(suit,value))
        return deck
    
    def shuffle(self):
        random.shuffle(self.__cards) 
        
    def deal(self):
        if len(self.__cards)>0:
            return self.__cards.pop()
        else:
            for _ in range(self.__n_decks):
                self.__cards.extend(self.__make_deck()) 
            self.shuffle()
            return self.__cards.pop()
############################################################ code that I added in starts    
    def get_cards(self):
        return self.__cards
    
    def n_cards(self):
        return len(self.__cards)
    
    def empty_deck(self):
        self.__cards = []
        
    def insert_cards(self,card):
        self.__cards.append(card)
        
        
    def copy(self):
        copy_deck = Deck()
        copy_deck.empty_deck()
        for cards in self.__cards:
            copy_deck.insert_cards(cards)
        return copy_deck
    
    def filter(self,filter_function):
        out_deck = Deck()
        out_deck.empty_deck()
        if type(filter_function) is Card:
            for cards in self.__cards:
                if cards == filter_function:
                    out_deck.insert_cards(cards)
            return out_deck
        elif isinstance(filter_function,CardFilterFunction):
            for cards in self.__cards:
                if filter_function(cards):
                    out_deck.insert_cards(cards)
            return out_deck
        elif isinstance(filter_function, Deck):
            for cards in self.__cards:
                if cards in filter_function.get_cards():
                    out_deck.insert_cards(cards)
            return out_deck
        elif isinstance(filter_function, list):
            for cards in self.__cards:
                if cards in filter_function:
                    out_deck.insert_cards(cards)
            return out_deck
            
    def remove(self, filter_function):
        _deck = Deck()
        _deck.empty_deck()
        if type(filter_function) is Card:
            for cards in self.__cards:
                if cards == filter_function:
                    self.__cards.remove(cards)
                    
        elif isinstance(filter_function,CardFilterFunction):
            for cards in self.__cards:
                if not filter_function(cards):
                    _deck.insert_cards(cards)
            self.__cards = _deck.get_cards()
                    
                    
        elif isinstance(filter_function, Deck):
            for cards in self.__cards:
                if cards not in filter_function.get_cards():
                    _deck.insert_cards(cards)
            self.__cards = _deck.get_cards()
                    
        elif isinstance(filter_function, list):
            for cards in self.__cards:
                if cards not in filter_function:
                    _deck.insert_cards(cards)
            self.__cards = _deck.get_cards()
    def sub_deck(self, filter_function, remove=False):
        out_deck = self.filter(filter_function)
        if remove == True:
            self.remove(filter_function)
        return out_deck
    def prob(self,condition):
        total = self.n_cards()
        _ = self.sub_deck(condition)
        good_cards = _.n_cards()
        try:
            probability = good_cards/total
        except ZeroDivisionError:
            probability = 0
        return probability       
############################################################ code that I added in ends     

def calc_hand_value(hand):
    card_values = list(map(lambda card: card.numerical_value(),hand))

    n_As= len(list(filter(lambda x: x==1,card_values)))
    
    hand_value = sum(card_values)

    if n_As==0:
        return hand_value
    
    # Case the last Ace is a 1
    Ace_as_one = hand_value
    Ace_as_eleven = hand_value+10
    
    if Ace_as_eleven<=21:
        return Ace_as_eleven
    else:
        return Ace_as_one

    
class PlayerBase(base):
    def __init__(self, name, n_chips):
        base.__init__(self)
        self.__name = name
        self.__n_chips=n_chips
    
    def name(self):
        return self.__name
    
    def chips(self):
        return self.__n_chips
    
    def pay(self,value=2):
        self.__n_chips+=value

    def deduct(self,value=2):
        # Logic to check if negative?
        self.__n_chips-=value

    def play_hand(self, down_card, up_cards, seen_cards ):
        raise NotImplementedError
        
    def __str__(self):
        return self.__name + "("+ str(self.__n_chips) + ")"
    
    __repr__=__str__
    
class DealerPlayer(PlayerBase):
    def __init__(self,threshold=17):
        self.__threshold = threshold
        PlayerBase.__init__(self,"Mr. Dealer", 1000)

    def play_hand(self, down_card, up_cards, seen_cards, deck):
        hand_value = calc_hand_value([down_card] + up_cards)
        return hand_value < self.__threshold
        
class ConsolePlayer(PlayerBase):
    def play_hand(self, down_card, up_cards, seen_cards,deck):
        print("Down Card:", down_card)
        print("Up Cards:", up_cards)
        print("Seen Cards:", seen_cards)
        hit_str= input("Hit(Y/N):")
        return hit_str.upper()=="Y"

    
class Strategy_1_Player(PlayerBase):
    def play_hand(self, down_card, up_cards, seen_cards, deck):
        return True
############################################################ code that I added in starts
class Strategy_2_Player(PlayerBase):
    def __init__ (self, name, l_thresh=-2 , u_thresh=0):
        PlayerBase.__init__(self,name,100)
        self.l_thresh = l_thresh
        self.u_thresh = u_thresh
    
    def play_hand(self, down_card, up_cards, seen_cards, deck):
        hand = ([down_card] + up_cards)
        counter = 0
        for cards in hand:
            if cards.numerical_value() >=2 and cards.numerical_value()<=6:
                counter += 1
            elif cards.numerical_value() >=7 and cards.numerical_value() <=9:
                counter += 0
            elif cards.numerical_value() == 10 and cards.numerical_value() == 1:
                counter -= 1
        if counter > self.u_thresh:
            counter = 0
            return True
        elif counter <= self.l_thresh:
            counter = 0
            return False
        
class Strategy_3_Player(PlayerBase):
    def __init__(self, name, chips,threshold=3):
        self.threshold = threshold
        PlayerBase.__init__(self, name, chips)
    def play_hand(self, down_card, up_cards, seen_cards, deck):
        counter = 0
        for cards in seen_cards:
            if cards.numerical_value() == 10:
                counter += 1
            
        hand_value = calc_hand_value([down_card] + up_cards)
        if hand_value <= 11:
            return True
        elif counter >= self.threshold:
            return True
        else:
            return False
        
class Strategy_4_Player(PlayerBase):
    def __init__(self, name, chips, threshold=0.675):
        self.threshold = threshold
        PlayerBase.__init__(self, name, chips)
    def play_hand(self, down_card, up_cards, seen_cards, deck):
        hand_value = calc_hand_value([down_card] + up_cards)
        bust_threshold = 22-hand_value
        sim_deck = deck.copy()
        bust_prob = sim_deck.prob(CheckGrNumericalValue(bust_threshold))
        if bust_prob > self.threshold:
            return False
        else:
            return True
          
############################################################ code that I added in ends        
class DealerLikePlayer(PlayerBase):
    def __init__(self,name,chips,threshold=16):
        self.__threshold = threshold
        PlayerBase.__init__(self,name, chips)

    def play_hand(self, down_card, up_cards, seen_cards, deck):
        hand_value = calc_hand_value([down_card] + up_cards)
        return hand_value < self.__threshold


    
class Game(base):
    def __init__(self,n_decks=6):
        base.__init__(self,self.INFO)
        self.__n_decks=n_decks
        self.__players = list()
        self.__all_players = list()
        
        self.__shuffle = False
        
        
    def players(self):
        return self.__players
    
    def all_players(self):
        return self.__all_players

    def add_player(self,player):
        self.__players.append(player)
        self.__all_players.append(player)

    def deal_and_check_shuffle(self,deck):
        card = deck.deal()
        if card.shuffle_card():
            shuffle=True
            card = deck.deal()
        return card
    
    def show_status(self,hands,seen_cards):
        self.message(self.INFO,"----------------------------------------------------------------")
        self.message(self.INFO,"Hands:",hands)
        self.message(self.INFO,"Seen Cards:",seen_cards)
        self.message(self.INFO,"*************************************************")
        self.message(self.INFO,"Players:")
        self.message(self.INFO,"*************************************************")
        for i,player in enumerate(self.__all_players):
            self.message(self.INFO,i,":",player)
        self.message(self.INFO,"----------------------------------------------------------------")

        
    def play_game(self,n_hands):
        # Create Dealer
        self.add_player(DealerPlayer())
        
        deck = None
        self.__shuffle = False
        
        # TODO: Check that all players have chips... 
        
        for i_hand in range(n_hands):
            
            # Remove Players with no money
            self.__players = list(filter(lambda player: player.chips()>=2,self.__players))
            self.message(self.DEBUG,"n players, n all players",len(self.__players),len(self.__all_players))            
            self.message(self.DEBUG,"Starting Hand:",i_hand,"/",n_hands)
            # New Hand
            
            # Do we have a deck or have to shuffle?
            if deck is None or self.__shuffle:
                self.message(self.DEBUG,"Creating New Deck / Shuffling")
                deck = Deck()
                # Shuffle Cards
                deck.shuffle()
                seen_cards = list()
                self.__shuffle=False

            hands = list()

            # Deal Each Players Hand
            # Down card deal
            self.message(self.DEBUG,"Dealing Cards")
            for player_i,player in enumerate(self.__players):
                down_card = self.deal_and_check_shuffle(deck)
                up_cards = list()
                hands.append((down_card,up_cards))
                if player_i < len(self.__players)-1:
                    seen_cards.append(down_card)
                
            # Up card deal
            for (down_card,up_cards) in hands:
                up_cards.append(self.deal_and_check_shuffle(deck))                
                seen_cards.append(up_cards[-1])
                
            # TODO: Show hands...
            self.show_status(hands,seen_cards)
            
            # Play
            # Deals cards and asks players to hit/stay
            
            for player_i,((down_card,up_cards),player) in enumerate(zip(hands,self.__players)):
                self.message(self.DEBUG,"Asking Player",player_i,"to Play")
                self.message(self.DEBUG,"Player",player_i,"hand total:",calc_hand_value([down_card]+up_cards))
                hit = True
                this_hand_up_cards=list()
                while(hit):
                    hit = player.play_hand(down_card,up_cards,seen_cards,deck)

                    if hit:
                        self.message(self.DEBUG,"Player",player_i,"Hit")
                        card = self.deal_and_check_shuffle(deck)
                        up_cards.append(card)
                        this_hand_up_cards.append(card)
                        hand_value = calc_hand_value([down_card] + up_cards)
                        self.message(self.DEBUG,"Hand Value:",hand_value)
                        if hand_value < 21:
                            hit = True
                        else: 
                            hit = False
                            if hand_value > 21:
                                self.message(self.DEBUG,"Player",player_i,"Busted")     
                            else:
                                self.message(self.DEBUG,"Player",player_i,"Got 21")
                    else:
                        self.message(self.DEBUG,"Player",player_i,"Stay")

                seen_cards.append(down_card)
                seen_cards.extend(this_hand_up_cards)

            # Pay:
            # Compute the hand values
            hand_values = [calc_hand_value([hand[0]]+hand[1]) for hand in hands]

            self.message(self.DEBUG,"Hand Values",hand_values)
            
            # Determine who gets paid
            if hand_values[-1]==21:
                self.message(self.DEBUG,"Dealer Got 21")
                for player_i,(hand_value,player) in enumerate(zip(hand_values[:-1],self.__players[:-1])):
                    if hand_value==21:
                        self.message(self.DEBUG,"Player",player_i,"Got 21. Paying 3 chips.")
                        player.pay(3)
                    else:
                        self.message(self.DEBUG,"Player",player_i,"Busted or dealer won. Deducting 2 chips.")
                        player.deduct(2)
                    
            if hand_values[-1]>21:        
                self.message(self.DEBUG,"Dealer Busted")
                for player_i,(hand_value,player) in enumerate(zip(hand_values[:-1],self.__players[:-1])):
                    if hand_value==21:
                        self.message(self.DEBUG,"Player",player_i,"Got 21. Paying 3 chips.")
                        player.pay(3)
                    elif hand_value>21:
                        self.message(self.DEBUG,"Player",player_i,"Busted. Deducting 2 chips.")
                        player.deduct(2)
                    else:
                        self.message(self.DEBUG,"Player",player_i,"Paying 2 chips.")
                        player.pay(2)
                        
            if hand_values[-1]<21:
                self.message(self.DEBUG,"Dealer hand is:",hand_values[-1])
                for player_i,(hand_value,player) in enumerate(zip(hand_values[:-1],self.__players[:-1])):
                    if hand_value==21:
                        self.message(self.DEBUG,"Player",player_i,"Got 21. Paying 3 chips.")
                        player.pay(3)
                    elif hand_value>21:
                        self.message(self.DEBUG,"Player",player_i,"Busted. Deducting 2 chips.")
                        player.deduct(2)
                    elif hand_value >  hand_values[-1]:
                        self.message(self.DEBUG,"Player",player_i," hand was",hand_value, "versus Dealer hand",
                                     hand_values[-1],"Paying 2 chips.")
                        player.pay(2)
                    else:
                        self.message(self.DEBUG,"Player",player_i," hand was",hand_value, "versus Dealer hand",
                                     hand_values[-1],"Deducting 2 chips.")
                        player.deduct(2)