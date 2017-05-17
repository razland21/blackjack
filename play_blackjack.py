from random import shuffle
from math import ceil

deck_template = [('A','H'),(2,'H'),(3,'H'),(4,'H'),(5,'H'),(6,'H'),(7,'H'),(8,'H'),(9,'H'),(10,'H'),('J','H'),('Q','H'),('K','H'),
('A','D'),(2,'D'),(3,'D'),(4,'D'),(5,'D'),(6,'D'),(7,'D'),(8,'D'),(9,'D'),(10,'D'),('J','D'),('Q','D'),('K','D'),
('A','C'),(2,'C'),(3,'C'),(4,'C'),(5,'C'),(6,'C'),(7,'C'),(8,'C'),(9,'C'),(10,'C'),('J','C'),('Q','C'),('K','C'),
('A','S'),(2,'S'),(3,'S'),(4,'S'),(5,'S'),(6,'S'),(7,'S'),(8,'S'),(9,'S'),(10,'S'),('J','S'),('Q','S'),('K','S')]

deck = []

#main game data tracking
players = [{'name':'dealer', 'hand': [[]], 'money': 0, 'bet': [0], 'status': ['playing']}, 
	{'name':'player', 'hand': [[]], 'money': 100, 'bet': [0], 'status': ['playing']}]

#rules
#min_bet: int value
#win/blackjack/loss: multipliers
#doubling_allowed: list of cards where doubling down is allowed
#shuffle: min number of cards left in deck to be able to do another round (i.e. if current deck is less than this, then shuffle)
#num_decks: number of decks to be used in game

rules = {'min_bet': 1, 'win': 1, 'blackjack': 1.5, 'loss': -1, 'doubling_allowed': [10, 11], 'shuffle': 15, 'num_decks': 1}


#PLAYER NAME

def set_name(player_posn, name):
	"""
	Sets name of given player.
	Arguments:
	- player_posn: an int representing the player
	- name: a string representing the player's name
	"""
	players[player_posn]['name'] = name
	
	
def get_name(player_posn):
	"""
	Returns name of given player.
	Arguments:
	- player_posn: an int representing the player
	Returns:
	- a string representing the name of the player
	"""

	return players[player_posn]['name'].title()
	
	
#RULES MANAGEMENT

def print_double_str():
	"""
	Returns string representing the current values in doubling_allowed
	"""
	
	double_str = ""
	
	#prepare string for doubling rule
	if len(rules['doubling_allowed']) == 20:
		double_str = "any two cards"
	else:
		double_str = ", ".join(str(num) for num in rules['doubling_allowed'][0:-1])
		double_str += " and {}".format(rules['doubling_allowed'][-1])
	
	return double_str
	
def view_rules():
	"""
	Prints out rules currently set for game.
	"""
			
	print "\n***GAME RULES***\n"
	print "Goal: Get as close to 21 as you can without going over. If you get closer to 21 than the dealer does, you win.\n"
	print "- Minimum bet: ${}".format(rules['min_bet'])
	print "- Doubling allowed on {}. Only one additional card is given to you if you double.".format(print_double_str())
	print "- Number of decks used in game: {}".format(rules['num_decks'])
	print "- Deck is shuffled when it has less than {} cards remaining.".format(rules['shuffle'])
	print ""

def process_rule_change(rule, new_value):
	"""
	Changes the given rule to the given value.
	Arguments:
	- rule: string representing the rule to change. This must correspond to a key in the rules dictionary.
	- new_value: int or list representing new values
	Returns:
	- rule_changed: True if rule changed. False otherwise.
	"""
	
	rule_changed = False
	
	if rule not in rules.keys():
		print "That rule is invalid. No changes will be made."
	elif not new_value.isdigit():
			print "You must enter an integer greater than 0.\n"
	elif rule == "doubling_allowed":
		if int(new_value) > 4:
			print "You must enter one of the numbers above.\n"
			return rule_changed
		elif new_value == "1":
			rules[rule] = range(8,12)
		elif new_value == "2":
			rules[rule] = range(9,12)
		elif new_value == "3":
			rules[rule] = range(9,12)
		elif new_value == "4":
			rules[rule] = range(2,22)
		rule_changed = True
	else:
		rules[rule] = int(new_value)
		rule_changed = True

	return rule_changed
	
def change_rules():
	"""
	Give player option to change rules currently set for game.
	"""
	
	change = True
	
	while change:
		print "\nYou can change the following rules:"
		print "    1: Minimum bet"
		print "    2: Doubling rules"
		print "    3: Number of decks used in game"
		print "    4: Shuffling threshold"
		print "\nEnter number of rule to change or enter 'quit' to go back to the main menu."
		
		choice = raw_input(" > ").strip().lower()
		
		if choice == "1":
			print "\nCurrent minimum bet: ${}".format(rules['min_bet'])
			print "Enter a new minimum bet. It must be a positive integer."
			
			new_min_bet = raw_input(" > ").strip()
			
			if process_rule_change('min_bet', new_min_bet):
				print "\nThe minimum bet required is now ${}.".format(rules['min_bet'])

		elif choice == "2":
			print "Doubling is currently allowed on {}.".format(print_double_str())
			print "\nPick from one of the following rules:"
			print "    1: Double on 8, 9, 10, 11 only"
			print "    2: Double on 9, 10, 11 only"
			print "    3: Double on 10, 11 only"
			print "    4: Double on any two cards"
			
			new_doubling = raw_input(" > ").strip().lower()
			
			if process_rule_change('doubling_allowed', new_doubling):
				print "\nYou can now double down on {}.".format(print_double_str())
			
		elif choice == "3":
			print "\nCurrent number of decks used in game: {}".format(rules['num_decks'])
			print "Enter the number of decks you want to use. It must be a positive integer."
			
			new_num_decks = raw_input(" > ").strip()
			
			if process_rule_change('num_decks', new_num_decks):
				print "\nThe number of decks used in game is now {}.".format(rules['num_decks'])

		elif choice == "4":
			print "\nGame currently shuffles deck when it has less than {} cards.".format(rules['shuffle'])
			print "Enter a new shuffling threshold. It must be a positive integer."
			
			new_shuffle = raw_input(" > ").strip()
			
			if process_rule_change('shuffle', new_shuffle):
				print "\nThe new shuffling threshold is now {}.".format(rules['shuffle'])

		elif choice == "quit":
			change = False
		else:
			print "Sorry, I don't know what you mean by {}.".format(choice)


#SPLITTING

def check_split(player_posn, hand_num=0):
	"""
	Check whether player can split his/her hand.  Players can only split of the values of the two cards are exactly the same.
	Arguments:
	- player_posn: an int representing the player
	- hand: a list of cards representing the hand to add a card to
	Returns:
	- True if hand can be split. False otherwise.
	"""
	
	if len(players[player_posn]['hand'][hand_num]) > 2:
		return False
	else:
		return players[player_posn]['hand'][hand_num][0][0] == players[player_posn]['hand'][hand_num][1][0]

		
def split_hands(player_posn, hand_num=0):
	"""
	Splits the player's hand into two separate hands and create separate bets for each hand.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	# Split the hands.
	card = players[player_posn]['hand'][hand_num].pop()
	new_hand = []
	new_hand.append(card)

	players[player_posn]['hand'].append(new_hand)
	
	hit(player_posn, deck, hand_num)
	hit(player_posn, deck, -1)
	
	# Add new bet to bet list.  Assumes equal to bet of hand being split.
	players[player_posn]['bet'].append(players[player_posn]['bet'][hand_num])
	
	# Add new status to status list.
	players[player_posn]['status'].append('playing')

	

def process_split(player_posn, hand_num=0):
	"""
	This function runs when player selects option to split.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	
	if not check_split(player_posn):
		print "You cannot split this hand."
	elif not check_funding(player_posn, players[player_posn]['bet'][hand_num]*2):
		print "You don't have enough money for this... but we'll let you do it anyway."

	split_hands(player_posn, hand_num)
		
		
#DOUBLING

def check_double(player_posn, hand_num=0):
	"""
	Check whether player can double down on his/her hand.  Players can only double if the sum of the *original* hand equals one of the numbers in the 'doubling_allowed' rule.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	
	return sum_cards(player_posn, hand_num) in rules['doubling_allowed'] and len(get_hand(player_posn, hand_num)) == 2

	
def process_double(player_posn, hand_num=0):
	"""
	This function runs when player selects option to double.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	
	if not check_double(player_posn, hand_num):
		print "{}, you cannot double down on this hand.".format(get_name(player_posn))
		return
	elif not check_funding(player_posn, get_bet(player_posn, hand_num)*2):
		print "{}, you don't have enough money for this... but we'll let you do it anyway.".format(get_name(player_posn))
	
	set_bet(player_posn, get_bet(player_posn, hand_num)*2)
	change_player_status(player_posn, 'doubling', hand_num)
	hit(player_posn, deck, hand_num)
	
	print_board(False, hand_num,len(get_hand(player_posn, hand_num))-1)
	print "\nHand is doubled. {}'s turn is over.".format(get_name(player_posn))

	if check_busted(player_posn, hand_num):
		change_player_status(player_posn, 'loss', hand_num) 
	else:
		change_player_status(player_posn, 'done', hand_num) 
	


#BETTING

def check_valid_bet(bet):
	"""
	Checks whether user input represents a valid bet
	Arguments:
	- move: string representing a bet
	Returns:
	- True if bet is valid. False otherwise.
	Assumptions:
	- bets must be integers greater than 1
	"""
	try:
		float(bet)
	except:
		print "You must enter a number greater than 0\n"
		return False
	if float(bet) < rules['min_bet']:
		print "You must bet at least ${}.\n".format(rules['min_bet'])
		return False
	else:
		return True

		
def check_funding(player_posn, bet):
	"""
	Checks whether player can afford placing the bet
	Arguments:
	- player_posn: an int representing the player
	- bet: int representing amount player wants to bet
	Returns:
	- True if bet can be made. False otherwise.
	"""
	
	return players[player_posn]['money'] >= bet

	
def get_bet(player_posn, bet_num=0):
	"""
	Get value of current bet for a player's hand
	Arguments:
	- player_posn: an int representing the player
	- bet_num: an int representing the position of the bet in the player's bet list. Default is 0 (first bet).

	"""
	
	return players[player_posn]['bet'][bet_num]

	
def set_bet(player_posn, bet, bet_num=0):
	"""
	Sets bet for player.
	Arguments:
	- player_posn: an int representing the player
	- bet: int representing amount player wants to bet
	- bet_num: an int representing the position of the bet in the player's bet list. Default is 0 (first bet).
	"""
	
	players[player_posn]['bet'][bet_num] = bet
	print "{} has bet ${} in this round for Hand {}.".format(get_name(player_posn),bet,bet_num+1)
	
	
def change_total_money(player_posn, amount):
	"""
	Changes total money available for player by given amount.
	Arguments:
	- player_posn: an int representing the player
	- amount: a float representing the amount that the player's total should change by
	"""
	
	print "\n{}'s previous total money: ${}".format(get_name(player_posn), players[player_posn]['money'])
	players[player_posn]['money'] += ceil(float(amount)*100)/100
	print "{}'s current total money: ${}\n".format(get_name(player_posn), players[player_posn]['money'])

	
def calculate_change(player_posn, rule, bet_num=0):
	"""
	Calculates how much the total money of a player should change by based on end result of game.
	Arguments:
	- player_posn: an int representing the player
	- rule: string representing the rule to follow (must be a key in 'rules' dictionary)
	- bet_num: an int representing the position of the bet in the player's bet list. Default is 0 (first bet).
	Returns:
	- total: the amount of money that needs to be added to a player's total. (negative number means it will be subtracted)
	"""

	total = 0
	
	if rule in rules:
		total = get_bet(player_posn, bet_num) * rules[rule]
	else:
		print "{} is an invalid rule. No change will be made to {}'s total".format(rule, get_name(player_posn))
	
	return ceil(float(total)*100)/100


#MAIN SUPPORTING FUNCTIONS

def shuffle_deck(deck_lst):
	"""
	Shuffles the game's deck of cards.
	Arguments: 
	- deck_lst: a list representing the deck of cards used during game
	"""
	
	#clear deck
	del deck_lst[0:]
	
	decks_added = 0
	
	while decks_added < rules['num_decks']:
		card_indices = range(52)
		shuffle(card_indices)
		
		for index in card_indices:
			deck_lst.append(deck_template[index])
		
		decks_added += 1
		
	print "Cards have been shuffled.\n"
	
	
def deal_cards(num_cards, deck_lst):
	"""
	Deals a given number of cards from the given card deck.
	Arguments: 
	- num_cards: an int representing the number of cards to deal
	- deck_lst: a list representing the current deck of cards
	Returns:
	- dealt_cards: a list of cards representing new cards to be added to a hand
	"""
	dealt_cards = []
	
	if len(deck_lst) < num_cards:
		shuffle_deck(deck_lst)
		
	while len(dealt_cards) < num_cards:
		dealt_cards.append(deck_lst.pop())
	
	return dealt_cards

	
def print_board(show_dealer_hand, hand_num="All", hidden_card="No"):
	"""
	Prints current game board.
	Arguments:
	- show_dealer_hand: a boolean representing whether to show or hide the dealer's first card. True = show card.
	- hand_num: an int representing the position of the hand in the player's hand list or a string representing all hands to be shown. Default is "All" (full list of hands).
	- hidden_card: an int representing the position of a card that should be hidden or a string representing all cards to be shown. Default is "No" (full list of cards).
	"""
	print "\n***DEALER***"
	if show_dealer_hand:
		print_hand(0)
		print "\nDealer Total: {}".format(sum_cards(0))

	else:
		print_hand(0, 0, 0)

	#only works for single player...probably need to pass in player as argument
	
	if type(hand_num) == int:
		print_player_board(1, hand_num, hidden_card)
	
	else:  #print all hands for player, assumes no need to hide any cards
		for num in range(len(get_hand(1))):
			print_player_board(1, num)
			
			
def print_player_board(player_posn, hand_num=0, hidden_card="No"):
	"""
	Prints board for a given player.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	- hidden_card: an int representing the position of a card that should be hidden or a string representing all cards to be shown. Default is "No" (full list of cards).
	"""
	
	print "\n\n***PLAYER {} - {} - HAND {}***".format(1,get_name(1).upper(),hand_num+1)
	print_hand(player_posn, hand_num, hidden_card)

	if get_player_status(player_posn, hand_num) != "doubling":
		print_total(player_posn, hand_num)
			
			
def print_total(player_posn, hand_num=0):
	"""
	Prints total of a hand for a given player.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	
	print "\nHand {} Total: {}\n".format(hand_num+1, sum_cards(player_posn, hand_num))		

	
def get_hand(player_posn, hand_num="All"):
	"""
	Returns a hand for a given player.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list or a string representing all hands to be shown. Default is "All" (full list of hands).
	Returns:
	- a list representing a specific hand for a player or list of lists if hand_num="All"
	"""
	if type(hand_num) == int:
		return players[player_posn]['hand'][hand_num]
	else:
		return players[player_posn]['hand']
		

def print_hand(player_posn, hand_num=0, hidden_card="No"):
	"""
	Print hand of player in picture form.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	- hidden_card: an int representing the position of a card that should be hidden or a string representing all cards to be shown. Default is "No" (full list of cards).
	"""
	
	hand = players[player_posn]['hand'][hand_num]
	hand_len = len(hand)
	
	print "  ______  " * hand_len
	print " |      | " * hand_len
	
	for card in hand:
		if type(hidden_card) == int and hand.index(card) == hidden_card:
			print " | X    |",
			continue
		elif card[0] == 10:
			print " | 10   |",
		else:
			print " | {}    |".format(card[0]),
	
	print ""
	print " |      | " * hand_len
	
	for card in players[player_posn]['hand'][hand_num]:
		if type(hidden_card) == int and hand.index(card) == hidden_card:
			print " |    X |",
		else:
			print " |    {} |".format(card[1]),
	
	print ""	
	print " |______| " * hand_len
	
	
def highest_sum_cards(player_posn, hand_num=0):
	"""
	Calculates highest possible sum of cards.  This is to determine how to handle Ace cards in hands. 
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	Returns:
	- sum_hand: sum of the values of all cards in hand
	"""
	
	sum_hand = 0
	added_ace = False
	
	for card in players[player_posn]['hand'][hand_num]:
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
	
	
def	sum_cards(player_posn, hand_num=0):
	"""
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	Returns:
	- sum_hand: sum of the values of all cards in hand
	Notes: 
	- A = 11 by default unless that causes player to bust. If multiple Aces in hand, all other Aces count as 1.
	"""
	sum_hand = highest_sum_cards(player_posn, hand_num)
	added_ace = has_ace(player_posn, hand_num)

	#check for overage caused by Ace and adjust
	if sum_hand > 21:
		if added_ace:
			sum_hand -= 10
		
	return sum_hand
	
	
def check_21(player_posn, hand_num=0):
	"""
	Checks whether the given player's hand has a value of 21.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	Returns:
	- True if value of hand is 21. False otherwise.
	"""
	
	return sum_cards(player_posn, hand_num) == 21

def check_blackjack(player_posn):
	"""
	Check if a player has blackjack. Blackjack only happens during initial card dealing (i.e. first hand)
	Arguments:
	- player_posn: an int representing the player
	Returns:
	- True if player meets conditions of blackjack. False otherwise.
	"""
	return check_21(player_posn) and len(get_hand(player_posn)) == 1 and len(get_hand(player_posn, 0)) == 2
	
def check_anyone_has_21():
	"""
	This check only happens at the beginning of each game - assumes looking at first hand only of each player.
	Returns:
	- True if anyone has 21. False otherwise.
	Note:
	- Currently only works for single player.
	"""
	dealer_has_21 = check_21(0)
	player_has_21 = check_21(1)
	
	if dealer_has_21 or player_has_21:	
		if dealer_has_21 and player_has_21:
			print "Both of you have 21.  Draw."
			change_player_status(1,'draw')
		elif dealer_has_21:
			change_player_status(1,'loss')
		elif player_has_21:
			change_player_status(1,'win')
		return True
	else:
		return False

def has_ace(player_posn, hand_num=0):
	"""
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	Returns:
	- True if at least one Ace card exists in the hand. False otherwise.
	"""
	
	for card in players[player_posn]['hand'][hand_num]:
		if 'A' in card:
			return True
			
	return False

def check_busted(player_posn, hand_num=0):
	"""
	Checks if value of player's hand is greater than 21.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	Returns:
	- True if hand is greater than 21. False otherwise.
	"""
	
	return sum_cards(player_posn, hand_num) > 21
	
		
def hit(player_posn, deck_lst, hand_num=0):
	"""
	Adds one card from the deck into a player's hand.
	Arguments:
	- player_posn: an int representing the player
	- deck_lst: a list representing the deck of cards used during game
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	
	#Note: deal_cards() returns a list of one card - [0] is added to append the card itself to the hand
	
	players[player_posn]['hand'][hand_num].append(deal_cards(1, deck_lst)[0])

	
def deck_needs_shuffling(deck_lst):
	"""
	Checks whether the deck needs to be shuffled based on current rule in rules['shuffle'].
	Arguments:
	- deck_lst: a list representing the deck of cards used during game
	Returns:
	- True if the deck needs to be shuffled.  False otherwise.
	"""
	
	return len(deck_lst) < rules['shuffle']
	
def print_options(player_posn, hand_num=0):
	"""
	Prints player's options.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	print "Choose from the following options:"
	print "    1 - Hit"
	print "    2 - Stand"
	if check_double(player_posn, hand_num):
		print "    3 - Double"
	if check_split(player_posn, hand_num):
		print "    4 - Split"
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
	elif int(move) > 4:
		print "You must enter one of the numbers above."
		return False
	else:
		return True

def check_soft_17(player_posn, hand_num=0):
	"""
	Check if a player's hand is a soft 17 (i.e. hand is 17 because A = 11)
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""
	
	return highest_sum_cards(player_posn, hand_num) == 17 and has_ace(player_posn, hand_num)
		
def dealer_must_hit():
	"""
	Checks if dealer must hit. Dealer must hit if their total is < 17 or if dealer has soft 17.
	Returns:
	- True if dealer must hit. False otherwise.
	"""
	
	#return True if dealer has soft 17
	if check_soft_17(0):
		return True
	else:
		return sum_cards(0) < 17

def check_dealer_won(player_posn, hand_num):
	"""
	Check if dealer won a given hand
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	Returns:
	- True if dealer won. False otherwise.
	"""
	
	return sum_cards(player_posn, hand_num) < sum_cards(0) and not check_busted(0)
	
	
def check_winner():
	"""
	Checks who won the game. Currently only works for single player.
	Note: 0 = dealer. 1 = player.
	"""
	print "----------------------"
	print " *** GAME RESULTS ***"
	print "----------------------\n"
	
	for hand_index in range(len(get_hand(1))):
		print "PLAYER {} - {} - HAND {}:".format(1, get_name(1).upper(), hand_index+1)
		
		if check_busted(1, hand_index):
			print "Busted! You lose."
			change_total_money(1, calculate_change(1,'loss', hand_index))
		
		elif get_player_status(1, hand_index) == 'loss':
			if check_21(0):
				print "Sorry, dealer has 21.  You lose."
			else: 
				print "You lose."
			change_total_money(1, calculate_change(1,'loss', hand_index))

		elif check_dealer_won(1, hand_index):
			print "Sorry, dealer won."
			change_total_money(1, calculate_change(1, 'loss', hand_index))

		elif sum_cards(1, hand_index) == sum_cards(0):
			print "Push.\n"

		elif check_blackjack(1):
			print "Player has Blackjack! You win!"
			change_total_money(1, calculate_change(1,'blackjack', hand_index))
			
		else:
			if check_busted(0):				
				print "Dealer busted! Player wins!"
				
			elif sum_cards(1, hand_index) > sum_cards(0):
				print "Congratulations, player wins!"
				
			change_total_money(1, calculate_change(1, 'win', hand_index))

			
def change_player_status(player_posn, status, hand_num=0):
	"""
	Change player's status.
	Arguments:
	- player_posn: an int representing the player
	- status: a string representing the player's current game status
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand)
	"""
	
	players[player_posn]['status'][hand_num] = status

	
def get_player_status(player_posn, hand_num=0):
	"""
	Return player's current status.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand)
	Returns:
	- string representing player's current status
	"""
	return players[player_posn]['status'][hand_num]

	
def reset_board():
	"""
	Reset the elements of the board for the next round.  
	Keeps total money intact.
	"""
	
	for index in range(len(players)):
		players[index]['hand'] = [[]]	
		players[index]['bet'] = [0]
		players[index]['status'] = ["playing"]

		
def process_hit(player_posn, hand_num=0):
	"""
	Player has requested to hit.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand)	
	"""
	
	print "\n{} hits.".format(get_name(player_posn))
	hit(player_posn, deck, hand_num)
	
	#if hitting due to a doubling move, do not show last card until game is over.
	if get_player_status(player_posn, hand_num) == "doubling":
		print_board(False, hand_num, len(get_hand(player_posn, hand_num))-1)
		print "Card dealt. {}'s turn is over.".format(get_name(player_posn))
	
	elif check_busted(player_posn, hand_num):
		print_board(False, hand_num) 
		print "Busted. {}'s turn is over.".format(get_name(player_posn))
		change_player_status(player_posn, 'loss', hand_num)
		
	elif check_21(player_posn, hand_num):
		print_board(False, hand_num)
		print "Total is 21. {}'s turn is over.".format(get_name(player_posn))
		change_player_status(player_posn, 'done', hand_num)

		
def dealer_play():
	"""
	Processes gameplay loop for dealer.
	"""
	
	print "\nDealer's Turn\n"
	
	while get_player_status(0) == 'playing':
		if dealer_must_hit():
			hit(0, deck)
		else:
			change_player_status(0, 'done')
	
	
	
def player_play(player_posn, hand_num=0):
	"""
	Processes gameplay loop for a single player.
	Arguments:
	- player_posn: an int representing the player
	- hand_num: an int representing the position of the hand in the player's hand list. Default is 0 (first hand).
	"""

		
	while get_player_status(player_posn, hand_num) == 'playing':
	
		print_board(False, hand_num)
		print "{}'s Turn - Hand {}\n".format(get_name(player_posn), hand_num+1)
		
		if check_21(player_posn, hand_num):
			change_player_status(player_posn, 'done', hand_num)
			print "Total is 21. {}'s turn is over.".format(get_name(player_posn))
		
		else:
			print_options(player_posn, hand_num)
			move = raw_input("Enter the number for the move you want to make: ").strip()
			
			#if move is not valid, start loop over
			if not check_valid_move(move):
				continue
		
			if move == "1":
				process_hit(player_posn, hand_num)
				
			elif move == "2":
				print "\n{} stands. Turn is over.".format(get_name(player_posn))
				change_player_status(player_posn,'done', hand_num) 
			
			elif move == "3":
				process_double(player_posn, hand_num)
			
			elif move == "4":
				process_split(player_posn, hand_num)
	


#MAIN GAME

def play_blackjack():
	"""
	Main function to run blackjack game.
	"""
	
	#*** GAME START ***
	
	#check if player's name is set - if not, ask for name
	
	if get_name(1) == 'Player':
		player_name = raw_input("What is your name? ").strip().lower()
		set_name(1, player_name)
	
	print "Minimum bet is ${}.".format(rules['min_bet'])
	print "{}'s total money: ${}\n".format(get_name(1),players[1]['money'])
	
	#reset board
	reset_board()
	
	#check if player has enough money, adds in $100 increments if not
	while not check_funding(1, rules['min_bet']):
		print "Oh no, you're broke! Let's fix that!"
		change_total_money(1, 100)
		
	#check if deck needs shuffling
	if deck_needs_shuffling(deck):
		shuffle_deck(deck)
	
	#betting loop: ask for bet/check validity/set bet		
	while True:
		bet = raw_input("Enter the amount you want to bet: ").strip()

		if check_valid_bet(bet):
			verified_bet = ceil(float(bet)*100)/100
			if check_funding(1, verified_bet):
				set_bet(1, verified_bet)
				break
			else:
				print "You do not have enough money to make that bet. Your current total is ${}.\n".format(players[1]['money'])
	
	#deal cards to all people in game
	for index in range(len(players)):
		players[index]['hand'][0] = deal_cards(2, deck)
				
	#check if anyone has 21
	check_anyone_has_21()
	
		
	#*** PLAYER GAME LOOP START ***
	
	#check if any player statuses are 'playing', if so, play that hand
	while 'playing' in players[1]['status']:
		player_play(1, players[1]['status'].index('playing'))
			
			
	#*** DEALER GAME LOOP START ***	
	
	#player status = done: player has finished turn but no conclusion on win/loss
	for status in players[1]['status']:
		if status == 'done':
			dealer_play()
			break
	
	print_board(True)
	check_winner()				
	

#START PROGRAM	

def print_main_menu():
	"""
	Print main menu options
	"""
	print "\nSelect from one of the following options:"
	print "    1: Play Blackjack"
	print "    2: View Rules"
	print "    3: Change Rules"
	print "    4: Quit"
	print ""


def start_game():
	"""
	Main function to start program
	"""
	print "\nWELCOME TO BLACKJACK!"
	
	while True:
		print_main_menu()
		
		choice = raw_input("Enter choice selection: ").strip().lower()
		if choice == "1":
			print "Alright, let's play!\n"
			play_blackjack()
		elif choice == "2":
			view_rules()
		elif choice == "3":
			change_rules()
		elif choice == "4":
			print "Thanks for playing!"
			break 
		else:
			print "Sorry, I'm not sure what you mean by {}.\n".format(choice)
	
	

#TESTS

start_game()

def set_hand(player_posn, card_list, hand_num=0):
	players[player_posn]['hand'][hand_num] = card_list


#####################################################################
# Doctest code

# if __name__ == '__main__':
    # import doctest
    # if doctest.testmod().failed == 0:
        # print "\n*** ALL TESTS PASSED. AWESOME WORK!\n"
