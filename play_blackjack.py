from random import randint

deck = [('A','H'),(2,'H'),(3,'H'),(4,'H'),(5,'H'),(6,'H'),(7,'H'),(8,'H'),(9,'H'),(10,'H'),('J','H'),('Q','H'),('K','H'),
('A','D'),(2,'D'),(3,'D'),(4,'D'),(5,'D'),(6,'D'),(7,'D'),(8,'D'),(9,'D'),(10,'D'),('J','D'),('Q','D'),('K','D'),
('A','C'),(2,'C'),(3,'C'),(4,'C'),(5,'C'),(6,'C'),(7,'C'),(8,'C'),(9,'C'),(10,'C'),('J','C'),('Q','C'),('K','C'),
('A','S'),(2,'S'),(3,'S'),(4,'S'),(5,'S'),(6,'S'),(7,'S'),(8,'S'),(9,'S'),(10,'S'),('J','S'),('Q','S'),('K','S')]

used_cards_indices = []
hands_dict = {'dealer': [], 'player': []}

total_money_dict = {'player': 100}
bets_dict = {'player': 1}

#BETTING

def check_valid_bet(bet):
	"""
	Checks whether user input represents a valid bet
	Arguments:
	- move: string representing a bet.
	Returns:
	- True if bet is valid. False otherwise.
	Assumptions:
	- bets must be integers greater than 1
	
	>>> check_valid_bet("aaa")
	You must enter an integer greater than 0.
	False
	>>> check_valid_bet("1.5")
	You must enter an integer greater than 0.
	False
	>>> check_valid_bet("2")
	True
	"""

	if not bet.isdigit():
		print "You must enter an integer greater than 0."
		return False
	elif int(bet) < 1:
		print "You must bet at least 1."
		return False
	else:
		return True

#MAIN SUPPORTING FUNCTIONS

def shuffle_deck(used_cards):
	"""
	Arguments: 
	- used_cards: a list of indices representing cards already used in deck
	"""
	del used_cards[0:]
	print "Cards have been shuffled."
	
def deal_cards(num_cards, used_cards):
	"""
	Arguments: 
	- num_cards: an int representing the number of cards to deal
	- used_cards: a list of indices representing cards already used in deck
	
	Returns:
	- cards: a list of cards representing new cards to be added to a hand
	"""
	cards = []
	
	while len(cards) < num_cards:
		new_card_index = randint(0,51)
		
		if not new_card_index in used_cards:
			used_cards.append(new_card_index)
			cards.append(deck[new_card_index])
	
	return cards
	
def print_board(all_hands, show_dealer_hand):
	"""
	Arguments:
	- all_hands: a dictionary representing all hands in current game
	- show_dealer_hand: a boolean representing whether to show or hide the dealer's first card. True = show card.
	Assumptions: 
	- If show_dealer_hand is False, then there are only two cards in deck (i.e. want to hide the first card)
	"""
	print "\n***DEALER***"
	if show_dealer_hand:
		for card in all_hands['dealer']:
			print_card(card)

		#line for test only - remove later.
		#print "\n[CHECK] Dealer Total: {}".format(sum_cards(all_hands['dealer']))

	else:
		print "XX",
		print_card(all_hands['dealer'][1])

		
	print "\n\n***PLAYER***"
	for card in all_hands['player']:
		print_card(card)

	#line for test only - remove later.
	#print "\n[CHECK] Player Total: {}".format(sum_cards(all_hands['player']))
		
	print "\n"
			
def print_card(card):
	"""
	Arguments:
	- card: a tuple representing a card. Cards are represented in tuples as (value, suit)
	"""
	print str(card[0]) + card[1],

def highest_sum_cards(hand):
	"""
	Calculates highest possible sum of cards.  This is to determine how to handle Ace cards in hands. 
	Arguments:
	- hand: a list of cards 
	Returns:
	- sum_hand: sum of the values of all cards in hand
	"""
	
	sum_hand = 0
	added_ace = False
	
	for card in hand:
		if card[0] in ['J', 'Q', 'K']:
			sum_hand += 10
		elif card[0] == 'A':
			if added_ace:
				sum_hand += 1
			else:
				added_ace = True
				sum_hand += 11
		else:
			sum_hand += card[0]
	
	return sum_hand
	
def	sum_cards(hand):
	"""
	Arguments:
	- hand: a list of cards 
	Returns:
	- sum_hand: sum of the values of all cards in hand
	Assumptions: 
	- A = 11 by default. If multiple Aces in hand, all other Aces count as 1.
	
	>>> sum_cards([("A","H"),("A","D"),("A","S"),(10,"H")])
	13
	>>> sum_cards([("A","H"),("A","D"),(10,"H")])
	12
	>>> sum_cards([("A","H"),(2,"D"),(3,"H"),("A","S")])
	17
	"""
	sum_hand = highest_sum_cards(hand)
	added_ace = has_ace(hand)

	#check for overage caused by Ace and adjust
	if sum_hand > 21:
		if added_ace:
			sum_hand -= 10
		
	return sum_hand
	
def check_21(hand):
	"""
	Checks whether the given hand has a value of 21.
	Arguments:
	- hand: a list of cards 
	Returns:
	- True if value of hand is 21. False otherwise.
	"""
	
	return sum_cards(hand) == 21

def has_ace(hand):
	"""
	Arguments:
	- hand: a list of cards 
	Returns:
	- True if at least one Ace card exists in the hand. False otherwise.
	"""
	for card in hand:
		if 'A' in card:
			return True
			
	return False

def check_busted(hand):
	"""
	Checks if value of hand is greater than 21.
	Arguments:
	- hand: a list of cards 
	Returns:
	- True if hand is greater than 21. False otherwise.
	"""
	
	return sum_cards(hand) > 21
		
def hit(hand, used_cards):
	"""
	Adds one card from the deck into a hand.
	Arguments:
	- hand: a list of cards representing the hand to add a card to
	- used_cards: a list of indices representing cards already used in deck
	Notes:
	- deal_cards() returns a list of one card - [0] is added to append the card itself to the hand
	"""
	
	hand.append(deal_cards(1,used_cards)[0])

def deck_needs_shuffling(num_cards_used):
	"""
	Checks whether the deck needs to be shuffled based on current assumptions.
	Arguments:
	- num_cards_used: an int representing the number of cards already used
	Returns:
	- True if the deck needs to be shuffled.  False otherwise.
	Assumptions: 
	- deck needs to be shuffled if there are <12 cards remaining.  (this can change later with more players)
	"""
	
	return num_cards_used > 40
	
def print_options():
	"""
	Prints player's options.
	"""
	print "Choose from the following options:"
	print "    1 - Hit"
	print "    2 - Stand"

def check_valid_move(move):
	"""
	Checks whether user input represents a valid move
	Arguments:
	- move: string representing a move.
	Returns:
	- True if move is valid. False otherwise.
	"""
	
	if len(move) == 0:
		print "You have to put something."
		return False
	elif not move.isdigit():
		print "You must enter a number."
		return False
	elif int(move) > 2:
		print "You must enter one of the numbers above."
		return False
	else:
		return True

def check_soft_17(hand):
	"""
	Check if hand is a soft 17 (i.e. hand is 17 because A = 11)
	>>> check_soft_17([(2,"H"),("A","D"),("A","S"),(10,"H")])
	False
	>>> check_soft_17([("A","H"),("A","D"),(5,"H")])
	True
	>>> check_soft_17([("A","H"),(2,"D"),(3,"H"),("A","S")])
	True
	>>> check_soft_17([("A","H"),(4,"H"),("A","S"),("A","C")])
	True
	>>> check_soft_17([("A","H"),(3,"H"),("A","S"),("A","C")])
	False
	"""
	
	return highest_sum_cards(hand) == 17 and has_ace(hand)
		
def dealer_must_hit(hand):
	"""
	Checks if dealer must hit. Dealer must hit if their total is < 17 or if dealer has soft 17.
	Arguments:
	- hand: a list of cards representing the hand to add a card to
	Returns:
	- True if dealer must hit. False otherwise.
	
	>>> dealer_must_hit([("A","H"),(4,"H"),("A","S"),("A","C")])
	True
	>>> dealer_must_hit([("A","H"),(3,"H"),("A","S"),("A","C")])
	True
	>>> dealer_must_hit([(5,"H"),("A","D"),("A","S"),(10,"H")])
	False
	"""
	
	#check if soft 17, return True
	if check_soft_17(hand):
		return True
	else:
		return sum_cards(hand) < 17
	
def check_winner(all_hands):
	"""
	Checks who won the game.
	Arguments:
	- all_hands: a dictionary representing all hands in current game
	"""
	
	if check_busted(all_hands['dealer']):				
		print "Dealer busted! Player wins!"
	elif sum_cards(all_hands['player']) > sum_cards(all_hands['dealer']):
		print "Congratulations, player wins!"
	elif sum_cards(all_hands['player']) == sum_cards(all_hands['dealer']):
		print "Draw."
	else:
		print "Sorry, dealer won."


#MAIN GAME
def play_blackjack():
	"""
	Main function to run blackjack game.
	"""
	player_status = 'playing'
	
	#*** GAME START ***
	while True:
			
		#check if deck needs shuffling
		if deck_needs_shuffling(len(used_cards_indices)):
			shuffle_deck(used_cards_indices)
		
		#deal cards to all people in game
		for person in hands_dict:
			hands_dict[person] = deal_cards(2,used_cards_indices)
					
		#check if anyone has 21 
		has_21 = False
		for person in hands_dict:
			if check_21(hands_dict[person]):
				has_21 = True
				print_board(hands_dict,True)
				if person == 'dealer':
					print "Sorry, dealer has 21.  You lose."
				else:
					print "{} has Blackjack! You win!".format(person)
				
		if has_21:
			break
		
	#*** PLAYER GAME LOOP START ***
		
		while True:
			print_board(hands_dict, False)
			print "Player's Turn\n"
			print_options()
			move = raw_input("Enter the number for the move you want to make: ").strip()
			
			#if move is not valid, start loop over
			if not check_valid_move(move):
				continue
		
			if move == "1":
				print "\nPlayer hits."
				hit(hands_dict['player'], used_cards_indices)
				if check_busted(hands_dict['player']):
					print_board(hands_dict, True)
					print "Busted! You lose."
					player_status = 'lost'
					break
				elif check_21(hands_dict['player']):
					print_board(hands_dict, False)
					print "You have 21. Turn is over."
					break
				
			elif move == "2":
				print "\nPlayer stands. Turn is over."
				break
			
	#*** DEALER GAME LOOP START ***	
		
		if player_status != 'lost':
			print "Dealer's Turn\n"
			
		while True:
			if player_status == 'lost':
				break
			
			if dealer_must_hit(hands_dict['dealer']):
				hit(hands_dict['dealer'], used_cards_indices)
			
			else:
				print_board(hands_dict, True)
				check_winner(hands_dict)				
				break
		break
	
	#end game - prompt to replay
	while True:
		replay = raw_input("\nDo you want to play again?  Type 'yes' or 'no': ").strip().lower()
		if replay == "yes":
			print "Alright, let's play again!\n"
			play_blackjack()
			break
		elif replay == "no":
			print "Thanks for playing!\n"
			break 
		else:
			print "Sorry, I'm not sure what you mean by {}.".format(replay)
	
	

#TESTS
			
#play_blackjack()

#####################################################################
# Doctest code

if __name__ == '__main__':
    import doctest
    if doctest.testmod().failed == 0:
        print "\n*** ALL TESTS PASSED. AWESOME WORK!\n"
