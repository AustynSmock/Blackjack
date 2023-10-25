import random as r
from moneyfile import *

class Card:
    """
    This class stores the suit, rank and points for my cards
    """
    def __init__(self, rank, suit, points):
        """
        Constructor for the Card class
        """
        self.rank = rank
        self.suit = suit
        self.points = points 
        
    def showCard(self):
        """
        Method prints the card's attributes
        """
        print(str(self.rank) + " of " + str(self.suit))
        
class Deck: 
    """
    This class provides a 52-card playing deck
    """
    def __init__(self):
        self.deck = []
        suit = ["Diamonds", "Clubs", "Hearts", "Spades"]    # Suit list
        rank = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"] # rank list
        for i in rank:
            for j in suit:
                if i == "Jack" or i == "Queen" or i == "King" or i == "10": 
                    self.deck.append(Card(i, j, 10))
                elif i == "Ace":
                    self.deck.append(Card(i, j, 1))
                else:
                    self.deck.append(Card(i, j, int(i)))
                    
    def shuffleDeck(self):
        """
        Method shuffles deck
        """
        r.shuffle(self.deck)
    
    def dealCard(self):
        """
        Method deals card
        """
        return self.deck.pop()
    
class Hand:
    """
    This class stores the dealer’s hand and the player’s hand
    """
    def __init__(self):
        """
        Method creates a list to store dealer's and player's hand
        """
        self.hand = []
        
    def addCard(self, deck):
        """
        Method adds a new card
        """
        self.hand.append(deck.dealCard())
        
    def displayCard(self):
        """
        Method displays card
        """
        self.hand[0].showCard()
    
    def showHand(self):
        """
        Method shows hand
        """
        for card in self.hand:
            card.showCard()
            
    def calculatePoints(self):
        """
        Method calculates points
        """
        value = 0
        aces = []
        for card in self.hand:
            if card.points == "Ace":
                aces.append(card)
                value += 11
            else:
                value += card.points
        if len(aces) == 0:
            return value
        while len(aces) > 0:
            if value <= 21:
                return value
            else:
                value -= 10
                aces.pop()
        return value
    
def welcome_message():
    """
    This function creates the game welcome message
    """
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()
    
def more_chips():
    """
    This function asks user if they would like to buy more chips and checks the amount
    """
    money = read_money()
    if money < 5:
        chips = int(input("You're broke. Would you like to buy more chips?\n How many chips: "))
        
        # check input
        while chips > int(10000) or chips <= int(0):
            chips = int(input("Amount of chips must be greater than 0 and less than or equal to 10,000. Please try again.\n How many chips: "))
            print()
        new_money = money + chips
        write_money(str(new_money))
    else:
        new_money = money
    return new_money

# Generate both player's hands, automate the dealer's, and automate ace behavior for dealer.
def deal():
    """
    This function gets players and dealers hands, and creats ace behavior for the dealer
    """
    new_deck = Deck()
    new_deck.shuffleDeck()
    dealers_hand = Hand()
    players_hand = Hand()
    
    players_hand.addCard(new_deck)
    players_hand.addCard(new_deck)
    players_hand.addCard(new_deck)
    dealers_hand.addCard(new_deck)
    
    dealers_points = dealers_hand.calculatePoints()
    while dealers_points <= 17:
        dealers_hand.addCard(new_deck)
        dealers_points = dealers_hand.calculatePoints()
    return dealers_hand, players_hand, new_deck

def main():
    
    # displays the opening display
    welcome_message()
    
    try:
        money = read_money()
        print("Current money: ", money)
        more_chips()
    
    except FileNotFoundError:
        # Player's money
        money = int(input("Starting Money:\t"))
        
        # check if money is correct
        while money > 10000 or money <= 0:
            money = int(input("Starting money cannot be greater than 10,000 or less than or equal to 0. Try again: "))
            print()
        write_money(str(money))
      
    choice = "y"    
    while choice.lower() == "y":
        # Create both player's hands of cards
        dealers_hand, players_hand, deck = deal()
        players_points = players_hand.calculatePoints()
        dealers_points = dealers_hand.calculatePoints()
        
        # Betting
        while True:
            try:                                             # try clause
                bet_amount = float(input("Bet Amount: "))    # prompt user for bet amount
            except ValueError:                               # except ValueError clause
                print("Invalid entry. Please try again.")    # prints if invalid entry is inputted 
                continue
            while(bet_amount < 5 or bet_amount > 1000):   # checks if user input for bet amount is more than 5 and less than 1000
                bet_amount = float(input("Bet amount has to be more than 5 and less than 1000: "))
            while(bet_amount > money):                    # checks if user input for bet amount is less than players total money
                bet_amount = float(input("Bet amount cannot exceed current money. Please try again: "))
            break
        # Automate dealer bust
        if dealers_points > 21:
            print("Dealer bust! You win!")
            print()
            # Winning screen 
            print("DEALER'S CARDS:")
            dealers_hand.showHand()
     
            print("\nYOUR CARDS:")
            players_hand.showHand()
            money += bet_amount
            write_money(str(money))
            print(money)

            choice = input("Play again? (y/n): ")
            if choice.lower == "n":
                break
            else:
                continue

        # Game 
        print("DEALER'S SHOW CARD:")
        dealers_hand.displayCard()

        print("\nYOUR CARDS:")
        players_hand.showHand()
        
        # Hit or Stand
        hitOrStand = input("Hit or stand? (hit/stand): ")
        # Hit allows the player to add a card to their hand
        while hitOrStand.lower() == "hit":
            players_hand.addCard(deck)
            players_hand.showHand()
            players_points = players_hand.calculatePoints()
            
            # Check if player busts with new card. 
            if players_points > 21: 
                print("You busted! :(")
                money -= bet_amount
                write_money(str(money))
                more_chips()
                print(money)
                #Check if player wants to play again if they bust (lose)
                choice = input("Play again? (y/n): ")
                if choice.lower == "n":
                    break
                else:
                    hitOrStand = "out"
            else:
                hitOrStand = input("Hit or stand? (hit/stand): ")
            
        if hitOrStand.lower() == "stand":
            print("DEALER'S CARDS:")
            dealers_hand.showHand()
            
            #End Game Screen
            print("\nYOUR CARDS")
            players_hand.showHand()
            print("YOUR POINTS:\t", players_points)                                    
            print("DEALER'S POINTS:", dealers_points)
            
            if players_points == dealers_points:
                print("You pushed!")
                money = money
                write_money(str(money))
                choice = input("Play again? (y/n)")
                if choice.lower == "n":
                    break
                else:
                    continue
            if players_points > dealers_points and players_points < 21:
                print("You win!")
                money += bet_amount
                write_money(str(money))
                print("Money: ", money)
                choice = input("Play again? (y/n)")
                if choice.lower == "n":
                    break
                else:
                    continue
            if players_points < dealers_points and players_points < 21:
                print("You lost!")
                money -= bet_amount
                
                write_money(str(money))
                
                money = more_chips()
                print("Money: ", money)
                choice = input("Play again? (y/n)")
                if choice.lower == "n":
                    break
                else:
                    continue
            if players_points == 21:
                print("You got a Blackjack!!")
                money += bet_amount * 1.5
                write_money(str(money))
                print("Money: ", money)
                choice = input("Play again? (y/n)")
                if choice.lower == "n":
                    break
                else:
                    continue  
    print("Bye!")
        
if __name__ == "__main__":
    main()
