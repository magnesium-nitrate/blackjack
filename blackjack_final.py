import cards as c
import games as g
import time

#players = {'name'=,'bank'=,'hand'=}

class Card(object):
	""" A playing card. """
	RANKS = ["A", "2", "3", "4", "5", "6", "7",
			 "8", "9", "10", "J", "Q", "K"]
	SUITS = ["c", "d", "h", "s"]
	
	def __init__(self, rank, suit):
		self.rank = rank 
		self.suit = suit

	def __str__(self):
		rep = self.rank + self.suit
		return rep


class Hand(object):
	""" A hand of playing cards. """
	def __init__(self):
		self.cards = []
		self.val = 0
		self.bank = 100

	def __str__(self):
		if self.cards:
		   rep = ""
		   for card in self.cards:
			   rep += str(card) + "  "
		   print(self.val) 
		else:
			rep = "<empty>"
		return rep
	def value(self,val):
		self.val = val
	def bankch(self,bet):
		self.bank = self.bank + bet

	def rval(self):
		return self.val
	def rbank(self):
		return self.bank
	def clear(self):
		self.cards = []

	def add(self, card):
		self.cards.append(card)

	def give(self, card, other_hand):
		self.cards.remove(card)
		other_hand.add(card)

class Deck(Hand):
	""" A deck of playing cards. """
	def populate(self):
		for suit in Card.SUITS:
			for rank in Card.RANKS: 
				self.add(Card(rank, suit))

	def shuffle(self):
		import random
		random.shuffle(self.cards)

	def deal(self, hands, per_hand = 1):
		for rounds in range(per_hand):
			for hand in hands:
				if self.cards:
					top_card = self.cards[0]
					self.give(top_card, hand)
				else:
					print("Can't continue deal. Out of cards!")


class Unprintable_Card(Card):
	""" A Card that won't reveal its rank or suit when printed. """
	def __str__(self):
		return "<unprintable>"


class BJ_Card(Hand):
	""" A Blackjack Card. """
	ACE_VALUE = 0
	value=0
	def get_value(self):
		ACE_VALUE = 0
		value=0
		for cards in self.cards:
			if((cards.rank>="2")and(cards.rank<="9")):
				value += int(cards.rank)
			elif(cards.rank!="A"):
				value += 10
			elif (cards.rank=="A"):
				value += 11
				ACE_VALUE = ACE_VALUE + 1

			else:
				print("yeet")
				#value = None
		if((value>21)and(ACE_VALUE!=0)):
			while((ACE_VALUE!=0)and(value>21)):
				value=value-10
				ACE_VALUE+=-1
		return value

	value = property(get_value)


class Positionable_Card(Card):
	""" A Card that can be face up or face down. """
	def __init__(self, rank, suit, face_up = True):
		super(Positionable_Card, self).__init__(rank, suit)
		self.is_face_up = face_up

	def __str__(self):
		if self.is_face_up:
			rep = super(Positionable_Card, self).__str__()
		else:
			rep = "XX"
		return rep

	def flip(self):
		self.is_face_up = not self.is_face_up


def f(dealer):

	if((dealer.cards[0].rank=="A")and(dealer.rval()==21)):
		return 2
	elif((dealer.cards[1].rank=="A")and(dealer.rval()==21)):
		return 3
	elif(dealer.cards[1].rank=="A"):
		return 4
	else:
		return 5


def output(things):
	for thing in things.cards:
		print(thing,end=" ")
	print("")

def payout(your_hand,dealer,bet):
	print("The Dealer: ",end="")
	for j in dealer.cards:
		print(j,end=" ")
	print("You: ",end="")
	for j in your_hand.cards:
		print(j,end=" ")
	if((your_hand.rval()<22)and((your_hand.rval()>dealer.rval())or(dealer.rval()>21))):
		your_hand.bankch(bet)
		print("ya won")
	elif((your_hand.rval()<22)and(your_hand.rval()==dealer.rval())):
		your_hand.bankch(0)
		print("ya tied")
	else:
		your_hand.bankch(-1*bet)
		print("ya lost")

def playo(your_hand,deck1,dealer,tea):
		ans = input("do you wanna hit/stand/doubledown/surrender")
		print(ans)
		while((ans!='stand')and(your_hand.rval()<22)and(ans!='doubledown')and(ans!='surrender')):
			deck1.deal([your_hand],per_hand=1)
			your_hand.value(BJ_Card.get_value(your_hand))
			output(your_hand)
			#print(your_hand.rval())
			if(your_hand.rval()<22):
				ans = input("do you wanna hit")
			else:
				ans = "stand"
		if(ans=="doubledown"):
			deck1.deal([your_hand],per_hand=1)
			your_hand.value(BJ_Card.get_value(your_hand))
			dealer.value(BJ_Card.get_value(dealer))
			output(dealer)
			while(dealer.rval()<17):
				deck1.deal([dealer],per_hand=1)
				dealer.value(BJ_Card.get_value(dealer))
				output(dealer)
			payout(your_hand,dealer,tea*2)
		elif(ans=="surrender"):
			payout(your_hand,dealer,tea/2)
		else:
			dealer.value(BJ_Card.get_value(dealer))
			output(dealer)
			while(dealer.rval()<17):
				deck1.deal([dealer],per_hand=1)
				dealer.value(BJ_Card.get_value(dealer))
				output(dealer)
			payout(your_hand,dealer,tea)
	


 
def main():
	deck1 = Deck()
	print("Created a new deck.")
	print("Deck:")
	print(deck1)

	deck1.populate()
	print("\nPopulated the deck.")
	print("Deck:")
	print(deck1)

	deck1.shuffle()
	print("\nShuffled the deck.")
	print("Deck:")
	print(deck1)

	dealer = Hand()
	your_hand = Hand()
	hands = [dealer, your_hand]
	game = input("do you wanna play?")
	while((game!="no")and(your_hand.rbank()>0)):
		print("The amount of money you have: " + str(your_hand.rbank()))
		tea = int(input("how much you bettin sis?"))
		deck1.deal(hands, per_hand = 2)
		print("\nDealt 2 cards to my hand and your hand.")
		print("DEALER: XX, ",end="")
		#your_hand.clear()
		#card2 = Card(rank = "A", suit = "c")
		#card3 = Card(rank = "10", suit = "s")
		#your_hand.add(card2)
		#your_hand.add(card3)
		#dealer.clear()
		#card4 = Card(rank = "10", suit = "c")
		#card5 = Card(rank = "A", suit = "s")
		#dealer.add(card4)
		#dealer.add(card5)
		print(dealer.cards[1])
		print("Your hand: ",end="")
		output(your_hand)

		your_hand.value(BJ_Card.get_value(your_hand))
		dealer.value(BJ_Card.get_value(dealer))
		if((your_hand.rval()!=21)and(f(dealer)==5)):
			playo(your_hand,deck1,dealer,tea)



			print(str(your_hand.rval()) +" "+ str(dealer.rval()))

		elif(((f(dealer)==3)or(f(dealer)==4))):
			if(your_hand.rval()!=21):
				x=input("do you want insurance, coward")
				if((x=="no")and(f(dealer)==4)):
					print("good choice sis")
					playo(your_hand,deck1,dealer,tea)
				elif((x=="no")and(f(dealer)==3)):
					print("tea,,,you lost")
					output(dealer)
					payout(your_hand,dealer,tea)
				elif((x=="yes")and(f(dealer)==4)):
					print("ya got scammed,, yikes")
					your_hand.bankch(-1*tea/2)
				else:
					print("oh ok wig you got it right")
			else:
				x=input("do you want even money?")
				if((x=="no")and(f(dealer)==4)):
					print("good choice sis")
					playo(your_hand,deck1,dealer,tea*1.5)
				elif((x=="no")and(f(dealer)==3)):
					print("tea,,,you tied")
					output(dealer)
					payout(your_hand,dealer,tea)
				elif((x=="yes")and(f(dealer)==4)):
					print("ya got scammed,, yikes")
					your_hand.bankch(tea)
				else:
					print("oh ok wig you got it right")
					your_hand.bankch(tea)
                                

		elif(f(dealer)==2):
			print("yikes sis you lost and that's that on that :/")
			your_hand.bankch(-1*tea)
		else:
			print("natural blackjack? it's more likely than you think")
			payout(your_hand,dealer,tea*1.5)

		game = input("continue?")
		dealer.clear()
		your_hand.clear()



	print("uwu")
	#time.sleep(5)



	print("Deck:")
	print(your_hand.rval())
	deck1.clear()
	print("\nCleared the deck.")
	print("Deck:", deck1)



main()
