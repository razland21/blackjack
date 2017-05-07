from random import randint

deck = [('A','H'),(2,'H'),(3,'H'),(4,'H'),(5,'H'),(6,'H'),(7,'H'),(8,'H'),(9,'H'),(10,'H'),('J','H'),('Q','H'),('K','H'),
('A','D'),(2,'D'),(3,'D'),(4,'D'),(5,'D'),(6,'D'),(7,'D'),(8,'D'),(9,'D'),(10,'D'),('J','D'),('Q','D'),('K','D'),
('A','C'),(2,'C'),(3,'C'),(4,'C'),(5,'C'),(6,'C'),(7,'C'),(8,'C'),(9,'C'),(10,'C'),('J','C'),('Q','C'),('K','C'),
('A','S'),(2,'S'),(3,'S'),(4,'S'),(5,'S'),(6,'S'),(7,'S'),(8,'S'),(9,'S'),(10,'S'),('J','S'),('Q','S'),('K','S')]

#main game data tracking
used_cards_indices = []
players = {'dealer': {'hand': [], 'money': 0, 'bet': 0, 'status': 'playing'}, 
	'player': {'hand': [], 'money': 100, 'bet': 0, 'status': 'playing'}}
#rules
#min_bet: int value
#win/blackjack/loss: multipliers
#doubling_allowed: list of cards where doubling down is allowed
#shuffle: min number of cards already used before shuffling has to happen

rules = {'min_bet': 1, 'win': 1, 'blackjack': 1.5, 'loss': -1, 'doubling_allowed': [10, 11], 'shuffle': 40}



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
	
	>>> check_valid_bet("1")
	True
	>>> rules['min_bet'] = 2
	>>> check_valid_bet("1")
	You must bet at least $2.
	False
	>>> check_valid_bet("2")
	True
	"""

	if not bet.isdigit():
		print "You must enter an integer greater than 0.\n"
		return False
	elif int(bet) < rules['min_bet']:
		print "You must bet at least ${}.\n".format(rules['min_bet'])
		return False
	else:
		return True

def check_funding(name, bet):
	"""
	Checks whether player can afford placing the bet
	Arguments:
	- name: string representing the name of the player
	- bet: int representing amount player wants to bet
	Returns:
	- True if bet can be made. False otherwise.
	"""
	
	return players[name]['money'] >= bet

def set_bet(name, bet):
	"""
	Sets bet for player.
	Arguments:
	- name: string representing the name of the player
	- bet: int representing amount player wants to bet
	>>> print bets_dict['player']
	1
	>>> set_bet('player', 5)
	Player has bet $5 in this round.
	>>> print bets_dict['player']
	5
	"""
	
	players[name]['bet'] = bet
	print "{} has bet ${} in this round.".format(name.title(),bet)
	
def change_total_money(name, amount):
	"""
	Changes total money available for player by given amount.
	Arguments:
	- name: string representing the name of the player
	- amount: a float representing the amount that the player's total should change by
	"""
	
	print "\n{}'s previous total money: ${}".format(name.title(), players[name]['money'])
	players[name]['money'] += amount
	print "{}'s current total money: ${}\n".format(name.title(), players[name]['money'])

def calculate_change(name, rule):
	"""
	Calculates how much the total money of a player should change by based on end result of game.
	Arguments:
	- name: string representing the name of the player
	- rule: string representing the rule to follow (must be a key in 'rules' dictionary)
	Returns:
	- total: the amount of money that needs to be added to a player's total.  (negative number means it will be subtracted)
	"""

	total = 0
	
	if rule in rules:
		total = players[name]['bet'] * rules[rule]
	else:
		print "{} is an invalid rule. No change will be made to {}'s total".format(rule, name)
	
	return total




#MAIN SUPPORTING FUNCTIONS

def shuffle_deck(used_cards):
	"""
	Arguments: 
	- used_cards: a list of indices representing cards already used in deck
	"""
	del used_cards[0:]
	print "Cards have been shuffled.\n"
	
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
	
def print_board(all_players, show_dealer_hand):
	"""
	Arguments:
	- all_players: a dictionary representing all players in current game
	- show_dealer_hand: a boolean representing whether to show or hide the dealer's first card. True = show card.
	Assumptions: 
	- If show_dealer_hand is False, then there are only two cards in deck (i.e. want to hide the first card)
	"""
	print "\n***DEALER***"
	if show_dealer_hand:
		for card in all_players['dealer']['hand']:
			print_card(card)

		print "\n\nDealer Total: {}".format(sum_cards('dealer'))

	else:
		print "XX",
		print_card(all_players['dealer']['hand'][1])

		
	print "\n\n***PLAYER***"
	for card in all_players['player']['hand']:
		print_card(card)

	print "\n\nPlayer Total: {}\n".format(sum_cards('player'))
	

def print_hand(name, show_dealer_hand=True):
	"""
	Print hand of player in picture form
	"""
	hand = players[name]['hand']
	hand_len = len(hand)
	
	print "  ______  " * hand_len
	print " |      | " * hand_len
	
	for card in hand:
		if not show_dealer_hand and hand.index(card) == 0:
			print " | X    |",
			continue
		elif card[0] == 10:
			print " | 10   |",
		else:
			print " | {}    |".format(card[0]),
	
	print ""
	print " |      | " * hand_len
	
	for card in players[name]['hand']:
		if not show_dealer_hand and hand.index(card) == 0:
			print " |    X |",
		else:
			print " |    {} |".format(card[1]),
	
	print ""	
	print " |______| " * hand_len
			
			
		
	
	
def print_card(card):
	"""
	Arguments:
	- card: a tuple representing a card. Cards are represented in tuples as (value, suit)
	"""
	print str(card[0]) + card[1],

def highest_sum_cards(name):
	"""
	Calculates highest possible sum of cards.  This is to determine how to handle Ace cards in hands. 
	Arguments:
	- name: a string representing the name of player whose hand to check 
	Returns:
	- sum_hand: sum of the values of all cards in hand
	"""
	
	sum_hand = 0
	added_ace = False
	
	for card in players[name]['hand']:
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
	
def	sum_cards(name):
	"""
	Arguments:
	- name: a string representing the name of player whose hand to check  
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
	sum_hand = highest_sum_cards(name)
	added_ace = has_ace(name)

	#check for overage caused by Ace and adjust
	if sum_hand > 21:
		if added_ace:
			sum_hand -= 10
		
	return sum_hand
	
def check_21(name):
	"""
	Checks whether the given player's hand has a value of 21.
	Arguments:
	- name: a string representing the person whose hand to check
	Returns:
	- True if value of hand is 21. False otherwise.
	"""
	
	return sum_cards(name) == 21

def check_anyone_has_21():
	dealer_has_21 = check_21('dealer')
	player_has_21 = check_21('player')
	
	if dealer_has_21 or player_has_21:
		#single player - assuming game automatically over if one of them have 21, so show dealer hand
		print_board(players, True)
		
		if dealer_has_21 and player_has_21:
			print "Both of you have 21.  Draw."
		elif dealer_has_21:
			print "Sorry, dealer has 21.  You lose."
			change_total_money('player', calculate_change('player','loss'))
		elif player_has_21:
			print "Player has Blackjack! You win!"
			change_total_money('player', calculate_change('player','blackjack'))
		return True
	else:
		return False

def has_ace(name):
	"""
	Arguments:
	- name: a string representing the person whose hand to check
	Returns:
	- True if at least one Ace card exists in the hand. False otherwise.
	"""
	for card in players[name]['hand']:
		if 'A' in card:
			return True
			
	return False

def check_busted(name):
	"""
	Checks if value of player's hand is greater than 21.
	Arguments:
	- name: a string representing the person whose hand to check
	Returns:
	- True if hand is greater than 21. False otherwise.
	"""
	
	return sum_cards(name) > 21
		
def hit(name, used_cards):
	"""
	Adds one card from the deck into a player's hand.
	Arguments:
	- hand: a list of cards representing the hand to add a card to
	- used_cards: a list of indices representing cards already used in deck
	Notes:
	- deal_cards() returns a list of one card - [0] is added to append the card itself to the hand
	"""
	
	players[name]['hand'].append(deal_cards(1,used_cards)[0])

def deck_needs_shuffling(num_cards_used):
	"""
	Checks whether the deck needs to be shuffled based on current rule in rules['shuffle'].
	Arguments:
	- num_cards_used: an int representing the number of cards already used
	Returns:
	- True if the deck needs to be shuffled.  False otherwise.
	"""
	
	return num_cards_used > rules['shuffle']
	
def print_options():
	"""
	Prints player's options.
	"""
	print "Choose from the following options:"
	print "    1 - Hit"
	print "    2 - Stand"
	print ""

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

def check_soft_17(name):
	"""
	Check if a player's hand is a soft 17 (i.e. hand is 17 because A = 11)
	"""
	
	return highest_sum_cards(name) == 17 and has_ace(name)
		
def dealer_must_hit():
	"""
	Checks if dealer must hit. Dealer must hit if their total is < 17 or if dealer has soft 17.
	Arguments:
	- hand: a list of cards representing the hand to add a card to
	Returns:
	- True if dealer must hit. False otherwise.
	"""
	
	#check if soft 17, return True
	if check_soft_17('dealer'):
		return True
	else:
		return sum_cards('dealer') < 17
	
def check_winner():
	"""
	Checks who won the game.
	Arguments:
	- all_hands: a dictionary representing all hands in current game
	"""
	
	if sum_cards('player') < sum_cards('dealer') and not check_busted('dealer'):
		print "Sorry, dealer won."
		change_total_money('player', calculate_change('player', 'loss'))
	elif sum_cards('player') == sum_cards('dealer'):
		print "Draw.\n"
	else:
		if check_busted('dealer'):				
			print "Dealer busted! Player wins!\n"
		elif sum_cards('player') > sum_cards('dealer'):
			print "Congratulations, player wins!\n"
		change_total_money('player', calculate_change('player', 'win'))

def change_player_status(name, status):
	"""
	Change player's status
	"""
	players[name]['status'] = status

def get_player_status(name):
	return players[name]['status']

def reset_board():
	"""
	Reset the elements of the board for the next round.  Need to keep total money intact.
	"""
	for person in players:
		players[person]['hand'] = []
		players[person]['bet'] = 0
		players[person]['status'] = "playing"

def dealer_play():
	print "\nDealer's Turn\n"
	
	while get_player_status('dealer') == 'playing':
		if dealer_must_hit():
			hit('dealer', used_cards_indices)
		else:
			change_player_status('dealer', 'done')
	
	print_board(players, True)

def player_play():
	"""
	For now, assumes single player.  Probably will need to take player name as argument later when supporting multiplayer.
	"""
	while get_player_status('player') == 'playing':
		print_board(players, False)
		print "Player's Turn\n"
		print_options()
		move = raw_input("Enter the number for the move you want to make: ").strip()
		
		#if move is not valid, start loop over
		if not check_valid_move(move):
			continue
	
		if move == "1":
			print "\nPlayer hits."
			hit('player', used_cards_indices)
			if check_busted('player'):
				print_board(players, True)
				print "Busted! You lose."
				change_total_money('player', calculate_change('player','loss'))
				change_player_status('player', 'loss')
				
			elif check_21('player'):
				print_board(players, False)
				print "You have 21. Turn is over."
				change_player_status('player','done')
			
		elif move == "2":
			print "\nPlayer stands. Turn is over."
			change_player_status('player','done')

		
	

#MAIN GAME
def play_blackjack():
	"""
	Main function to run blackjack game.
	"""
	
	#*** GAME START ***
	print "Minimum bet is ${}.".format(rules['min_bet'])
	print "Player's total money: ${}\n".format(players['player']['money'])
	
	#reset board
	reset_board()
	
	#check if player has enough money
	if not check_funding('player', rules['min_bet']):
		print "Oh no, you're broke! Let's fix that!"
		change_total_money('player', 100)
		
	#check if deck needs shuffling
	if deck_needs_shuffling(len(used_cards_indices)):
		shuffle_deck(used_cards_indices)
	
	#betting loop: ask for bet/check validity/set bet		
	while True:
		bet = raw_input("Enter the amount you want to bet: ").strip()

		if check_valid_bet(bet):
			bet = int(bet)
			if check_funding('player', bet):
				set_bet('player', bet)
				break
			else:
				print "You do not have enough money to make that bet. Your current total is ${}.\n".format(players['player']['money'])
	
	#deal cards to all people in game
	for person in players:
		players[person]['hand'] = deal_cards(2,used_cards_indices)
				
	#check if anyone has 21
	if check_anyone_has_21():
		return
		
	#*** PLAYER GAME LOOP START ***
		
	player_play()
			
	#*** DEALER GAME LOOP START ***	
		
	if get_player_status('player') != 'loss':
		dealer_play()
		check_winner()				
	
		

def start_game():

	while True:
		choice = raw_input("Do you want to play Blackjack?  Type 'yes' or 'no': ").strip().lower()
		if choice == "yes":
			print "Alright, let's play!\n"
			play_blackjack()
		elif choice == "no":
			print "Thanks for playing!"
			break 
		else:
			print "Sorry, I'm not sure what you mean by {}.\n".format(choice)
	
	

#TESTS
			
start_game()

#####################################################################
# Doctest code

# if __name__ == '__main__':
    # import doctest
    # if doctest.testmod().failed == 0:
        # print "\n*** ALL TESTS PASSED. AWESOME WORK!\n"
