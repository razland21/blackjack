from random import randint

deck = [('A','H'),(2,'H'),(3,'H'),(4,'H'),(5,'H'),(6,'H'),(7,'H'),(8,'H'),(9,'H'),(10,'H'),('J','H'),('Q','H'),('K','H'),
('A','D'),(2,'D'),(3,'D'),(4,'D'),(5,'D'),(6,'D'),(7,'D'),(8,'D'),(9,'D'),(10,'D'),('J','D'),('Q','D'),('K','D'),
('A','C'),(2,'C'),(3,'C'),(4,'C'),(5,'C'),(6,'C'),(7,'C'),(8,'C'),(9,'C'),(10,'C'),('J','C'),('Q','C'),('K','C'),
('A','S'),(2,'S'),(3,'S'),(4,'S'),(5,'S'),(6,'S'),(7,'S'),(8,'S'),(9,'S'),(10,'S'),('J','S'),('Q','S'),('K','S')]


def shuffle_deck(used_cards):
	del used_cards[0:]
	print "Cards have been shuffled."
	

def deal_cards(num_cards, used_cards):
	cards = []
	
	while len(cards) < num_cards:
		new_card_index = randint(0,51)
		
		if not new_card_index in used_cards:
			used_cards.append(new_card_index)
			cards.append(deck[new_card_index])
	
	return cards

	
def print_board (all_hands, show_dealer_hand):
	"""
	Assumptions: if show_dealer_hand is False, then there are only two cards in deck (i.e. want to hide the first card)
	"""
	print "***DEALER***"
	if show_dealer_hand:
		for card in all_hands['dealer']:
			print_card(card)
	else:
		print "XX",
		print_card(all_hands['dealer'][1])

	print "\n\n***PLAYER***"
	for card in all_hands['player']:
		print_card(card)
	
	print "\n"

			
def print_card (card_tuple):
	"""
	Card is represented in tuple as (value, suit)
	"""
	print str(card_tuple[0]) + card_tuple[1],

"""			
[fn] check_21 (hand)
	sum_hand = sum_cards(hand)
	has_ace = False
	
	check if ace is in deck - if yes, has_ace = True
	
	if sum_hand = 21,
		return True
	if has_ace = True,
		check sum_hand-10 = 21
	else return False

[fn] check_busted (hand)
	if sum_cards(hand) > 21, return True

[fn] sum_cards (hand)
	sum_hand = 0
	for all cards in hand
		add value to hand
		if J/Q/K, add 10
		if A,
			add 11

	return sum_hand

[fn] print_options()
	Choose from the following options:
	1 - Hit
	2 - Stand

[fn] hit(hand)
	deal_cards(1) -- returns list of one card
	add card to deck 
	
[fn] check_winner(dealer_hand, player_hand)

"""


#MAIN GAME
def play_blackjack():

	used_cards_indices = []
	hands_dict = {'dealer': [], 'player': []}
	
	while True:
		print "Current Options:"
		print "1 - deal cards"
		print "2 - see used cards"
		print "3 - shuffle cards"
		print "4 - show current hand"
		print "5 - print board"
		print "0 - exit"
		
		option = int(raw_input("Enter number: "))
		
		if option == 1:
			num_cards = int(raw_input("How many cards? "))
			give_cards = raw_input("Who should cards go to? dealer or player ")
			hands_dict[give_cards] += deal_cards(num_cards, used_cards_indices)
			print "The current deck is {}".format(hands_dict[give_cards])
		elif option == 2:
			print used_cards_indices
		elif option == 3:
			shuffle_deck(used_cards_indices)
		elif option == 4:
			show_hand = raw_input("Whose hand do you want to see? dealer or player ")
			print hands_dict[show_hand]
		elif option == 5:
			print_board(hands_dict, True)
			print_board(hands_dict, False)
		else:
			break

			
play_blackjack()
"""			
code outline:

[fn] main function to start blackjack game

	[fn] shuffle deck if needed
	[fn] deal cards
	[fn] print game board -- showing player's 2 cards and dealer's 2nd card only
	[fn] check if player has 21 to start 
			- if yes, automatic win (later - draw if both have 21)
			- if no, continue
	[fn] check if dealer has 21 to start
			- if yes, automatic lose
	
	*** PLAYER GAME LOOP START ***
	[fn] print gameplay options
			- hit
			- stand
			[more later]
	ask player to choose option
	
	if player chooses hit, give player another card.
		[fn] hit
		[*fn] print game board -- showing new card added to player's hand
		[*fn] check if player has 21 -- if yes, turn is over (not automatic win)
		[fn] check if player is over 21 -- if yes, automatic lose
	
	if player chooses stand, player turn ends.
	
	*** PLAYER GAME LOOP END ***
	
	*** DEALER GAME LOOP START ***
	[*fn] print game board -- show both of dealer's cards  [print game board needs to take y/n argument for showing dealer's other card]
			- if player has already lost, end here.
			
	[*fn] check if dealer is busted -- if yes, turn is over, player automatically wins
	[*fn] check if dealer has 17 
		- if yes, dealer's turn is over (not automatic win)
		- if no, hit again
	
	
	*** DEALER GAME LOOP END ***
			
	*** CHECK FOR WINNER ***
	if player already won/lost, then done.  
	else:
	[fn] check who has higher number, dealer or winner
"""