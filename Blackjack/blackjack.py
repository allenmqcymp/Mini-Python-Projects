from random import shuffle
import sys

''' Extensions:
    Use 6 decks of card instead of 1
    Ace cards can act both as a 1 and a 11
'''

'''

'''

class Card(object):
    def __init__(self, value):
        self.value = value
    def getValue(self):
        return self.value
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(self, other)

# Ace can either be a 1 or an 11
class Ace(Card):
    def __init__(self, value):
        Card.__init__(self, value)
    def set(self, value):
        if value == 11 or value == 1:
            self.value = value
        else:
            raise ValueError("Cannot assign number to ace card: must be 1 or 11")


class Hand(object):
    def __init__(self):
        self.hand = []
        self.empty = True
    def reset(self):
        self.__init__()
    def add(self, card):
        self.hand.append(card)
    def getCard(self, i):
        return self.hand[i]

    def getTotalValue(self):
        value = 0
        for card in self.hand:
            value += card.getValue()
        return value

    def contains(self, card):
        return card in self.hand

    # should return the list in place
    def getHand(self):
        return self.hand

    def toString(self):
        print "Value of hand:"
        for card in self.hand:
            print(card.value)

class Deck(object):
    def __init__(self):
        self.deck = []
        self.build()
        self.shuffle()

    def build(self):
        for deck in range(0, 6):
            for repeat in range(0, 4):
                for i in range(1, 10):
                    self.deck.append(Card(i))
            for tenc in range (0, 12):
                self.deck.append(Card(10))
            for i in range(0, 4):
                self.deck.append(Ace(11))

    def deal(self):
        return self.deck.pop(0)

    def pick(self, i):
        return self.deck.pop(i)

    def shuffle(self):
        return shuffle(self.deck)

    def toString(self):
        print "Deck"
        for card in self.deck:
            print(card.value)

    def getDeckSize(self):
        return len(self.deck)

class Blackjack(object):
    def __init__(self, reshuffleCount):
        self.reset(newDeck=True)
        self.playerHand = Hand()
        self.dealerHand = Hand()
        self.playerScore = 0
        self.dealerScore = 0
        self.deck = Deck()
        self.reshuffleCount = reshuffleCount
        # 0 is push; 1 if player wins; -1 if dealer wins
        self.number = 0

    def reset(self, newDeck):
        if newDeck:
            self.deck = Deck()
            shuffle(self.deck.deck)
        self.playerScore = 0
        self.dealerScore = 0
        self.playerHand = Hand()
        self.dealerHand = Hand()

    def deal(self):
        self.playerHand.add(self.deck.deal())
        self.dealerHand.add(self.deck.deal())
        self.playerScore = self.playerHand.getTotalValue()
        self.dealerScore = self.dealerHand.getTotalValue()


    def toString(self):
        print "State of game"
        print "--------------"
        print "Number of cards in the deck: %d" % self.deck.getDeckSize()
        for (i, card) in enumerate(self.playerHand.hand):
            print "Player Card: %s \n" % (card.getValue())
        print "The player's score: %s\n" % (self.playerScore)
        for (i, card) in enumerate(self.dealerHand.hand):
            print "Dealer Card: %s \n" % (card.getValue())
        print "The dealer's score: %s\n" % (self.dealerScore)
        print "------------\n"


    def playerTurn(self):
        while not self.playerHand.getTotalValue() >= 16:
            self.playerHand.add(self.deck.deal())
            self.playerScore = self.playerHand.getTotalValue()
        self.changeAce(self.playerHand)
        self.playerScore = self.playerHand.getTotalValue()
        if self.playerScore > 21:
            return False
        else:
            return True

    def dealerTurn(self):
        while not self.dealerHand.getTotalValue() >= 17:
            self.dealerHand.add(self.deck.deal())
            self.dealerScore = self.dealerHand.getTotalValue()
        self.changeAce(self.dealerHand)
        self.dealerScore = self.dealerHand.getTotalValue()
        if self.dealerScore > 21:
            return False
        else:
            return True

    def getResult(self):
        return self.main()

    def shuffleIfNeed(self):
        if self.deck.getDeckSize() == self.reshuffleCount:
            print "Shuffled!"
            # shuffle works in place and returns none
            shuffle(self.deck.deck)

    def changeAce(self, hand):
        if hand.getTotalValue() > 21 and hand.contains(Ace(11)):
            # change the value of the Ace to 1 in place
            index = hand.getHand().index(Ace(11))
            hand.getHand()[index] = Ace(1)
            print "Value changed"



    def main(self):

        self.reset(False)
        print(self.playerScore)

        # if new deck needed
        if self.deck.getDeckSize() <= 10:
            self.reset(True)

        print "Start of game\n"
        self.deal()

        self.shuffleIfNeed()

        self.toString()
        print "It's the player's turn\n"
        self.playerTurn()
        self.toString()

        if not self.playerTurn():
            print "The player lost (went bust)\n"
            self.number = -1
            return self.number

        self.shuffleIfNeed()

        self.dealerTurn()
        print "It's the dealer's turn\n"
        self.toString()

        if not self.dealerTurn():
            print "The dealer lost (went bust)"
            self.number = 1
        elif self.playerScore > self.dealerScore:
            print "The player's score: %s is higher than the dealer's score: %s" % \
                  (self.playerScore, self.dealerScore)
            print "The player won"
            self.number = 1
        elif self.dealerScore > self.playerScore:
            print "The dealer's score %s is higher than the player's score %s" % \
                  (self.dealerScore, self.playerScore)
            print "The dealer won"
            self.number = -1
        elif self.dealerScore == self.playerScore:
            print "It's a push!"
            self.number = 0

        return self.number

class Simulation(object):
    def __init__(self):
        self.playerWins = 0
        self.dealerWins = 0
        self.pushes = 0
    def main(self):
        standard_deck = 52
        game = Blackjack(standard_deck)
        for i in range(0, 1000):

            result = game.getResult()
            if result == -1:
                self.dealerWins += 1
            elif result == 1:
                self.playerWins += 1
            elif result == 0:
                self.pushes += 1
        print "After 1000 games"
        print "Player wins: %s" % (self.playerWins)
        print "Dealer wins %s" % (self.dealerWins)
        print "Pushes: %s\n" % (self.pushes)
        print "Dealer win percentage: %s" % (float(self.dealerWins) / 1000 * 100)
        print "Player win percentage: %s" % (float(self.playerWins) / 1000 * 100)



def main():
    # simulation = Simulation()
    # simulation.main()
    game = Blackjack(52)
    game.main()





if __name__ =="__main__":
    main()


