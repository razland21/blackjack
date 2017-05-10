from random import randint

deck = [('A','H'),(2,'H'),(3,'H'),(4,'H'),(5,'H'),(6,'H'),(7,'H'),(8,'H'),(9,'H'),(10,'H'),('J','H'),('Q','H'),('K','H'),
('A','D'),(2,'D'),(3,'D'),(4,'D'),(5,'D'),(6,'D'),(7,'D'),(8,'D'),(9,'D'),(10,'D'),('J','D'),('Q','D'),('K','D'),
('A','C'),(2,'C'),(3,'C'),(4,'C'),(5,'C'),(6,'C'),(7,'C'),(8,'C'),(9,'C'),(10,'C'),('J','C'),('Q','C'),('K','C'),
('A','S'),(2,'S'),(3,'S'),(4,'S'),(5,'S'),(6,'S'),(7,'S'),(8,'S'),(9,'S'),(10,'S'),('J','S'),('Q','S'),('K','S')]

#main game data tracking
used_cards_indices = []
players = {'dealer': {'hand': [[]], 'money': 0, 'bet': [0], 'status': ['playing']}, 
	'player': {'hand': [[]], 'money': 100, 'bet': [0], 'status': ['playing']}}

#rules
#min_bet: int value
#win/blackjack/loss: multipliers
#doubling_allowed: list of cards where doubling down is allowed
#shuffle: min number of cards already used before shuffling has to happen

rules = {'min_bet': 1, 'win': 1, 'blackjack': 1.5, 'loss': -1, 'doubling_allowed': [10, 11], 'shuffle': 40}

#SPLITTING

def check_split(name, hand_num=0):
	"""
	Check whether player can split his/her hand.  Players can only split of the values of the two cards are exactly the same.
	"""
	
	if len(players[name]['hand'][hand_num]) > 2:
		return False
	else:
		return players[name]['hand'][hand_num][0][0] == players[name]['hand'][hand_num][1][0]

		
def split_hands(name, hand_num=0):
	"""
	Split the hand into two separate hands and create separate bets for each hand.
	"""
	# Split the hands.
	card = players[name]['hand'][hand_num].pop()
	new_hand = []
	new_hand.append(card)

	players[name]['hand'].append(new_hand)
	
	hit(name, used_cards_indices, hand_num)
	hit(name, used_cards_indices, len(players[name]['hand'])-1)
	
	# Add new bet to bet list.  Assumes equal to bet of hand being split.
	players[name]['bet'].append(players[name]['bet'][hand_num])
	
	# Add new status to status list.
	players[name]['status'].append('playing')
	

def process_split(name, hand_num=0):
	"""
	Player has requested to split
	"""
	# TEMP: remove later.
	# print "You have requested to split...but this game doesn't do that yet. Please do something else."
	
	if not check_split(name):
		print "You cannot split this hand."
	elif not check_funding(name, players[name]['bet'][hand_num]*2):
		print "You don't have enough money for this... but we'll let you do it anyway."

	split_hands(name, hand_num)
	
	return
		
		
#DOUBLING

def check_double(name, hand_num=0):
	"""
	Check whether player can double down on his/her hand.  Players can only double if the sum of the *original* hand equals one of the numbers in the 'doubling_allowed' rule.
	"""
	
	return sum_cards(name, hand_num) in rules['doubling_allowed'] and len(players[name]['hand'][hand_num]) == 2

	
def process_double(name, hand_num=0):
	"""
	Player has requested to double
	Assumptions:
	- Assuming doubling on first hand.
	"""
	if not check_double(name, hand_num):
		print "You cannot double down on this hand."
		return
	elif not check_funding(name, get_bet(name, hand_num)*2):
		print "You don't have enough money for this... but we'll let you do it anyway."
	
	set_bet(name, get_bet(name, hand_num)*2)
	hit(name, used_cards_indices, hand_num)
	change_player_status(name, 'double', hand_num)
	print "Card dealt - turn is over."
	if check_busted(name, hand_num):
		print_board(True)
		print "Busted! You lose."
		change_total_money(name, calculate_change(name,'loss'), hand_num)
		change_player_status(name, 'loss', hand_num) 
	else:
		change_player_status(name, 'done', hand_num) 	
	


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

	
def get_bet(name, bet_num=0):
	"""
	Get value of current bet for a player's hand
	"""
	
	return players[name]['bet'][bet_num]

	
def set_bet(name, bet, bet_num=0):
	"""
	Sets bet for player.
	Arguments:
	- name: string representing the name of the player
	- bet: int representing amount player wants to bet
	"""
	
	players[name]['bet'][bet_num] = bet
	print "{} has bet ${} in this round for Hand {}.".format(name.title(),bet,bet_num+1)
	
	
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

	
def calculate_change(name, rule, bet_num=0):
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
		total = players[name]['bet'][bet_num] * rules[rule]
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
	
	
def print_board(show_dealer_hand, hand_num="All"):
	"""
	Arguments:
	- all_players: a dictionary representing all players in current game
	- show_dealer_hand: a boolean representing whether to show or hide the dealer's first card. True = show card.
	"""
	print "\n***DEALER***"
	if show_dealer_hand:
		print_hand('dealer')
		print "\nDealer Total: {}".format(sum_cards('dealer'))

	else:
		print_hand('dealer', 0)

	#to add: if player status = double, hide last card and total.	
	#only works for single player...probably need to pass in player as argument
	
	if type(hand_num) == int:
		print_player_board('player', hand_num)
	
	else:  #print all hands for player
		for num in range(len(players['player']['hand'])):
			print_player_board('player', num)
			
			
def print_player_board(name, hand_num=0):
			print "\n\n***PLAYER - HAND {}***".format(hand_num+1)
			print_hand('player','No', hand_num)

			print "\nHand {} Total: {}\n".format(hand_num+1, sum_cards('player', hand_num))		
			
			
def print_hand(name, hide_card="No", hand_num=0):
	"""
	Print hand of player in picture form
	"""
	hand = players[name]['hand'][hand_num]
	hand_len = len(hand)
	
	print "  ______  " * hand_len
	print " |      | " * hand_len
	
	for card in hand:
		if type(hide_card) == int and hand.index(card) == hide_card:
			print " | X    |",
			continue
		elif card[0] == 10:
			print " | 10   |",
		else:
			print " | {}    |".format(card[0]),
	
	print ""
	print " |      | " * hand_len
	
	for card in players[name]['hand'][hand_num]:
		if type(hide_card) == int and hand.index(card) == hide_card:
			print " |    X |",
		else:
			print " |    {} |".format(card[1]),
	
	print ""	
	print " |______| " * hand_len
	
	
def highest_sum_cards(name, hand_num=0):
	"""
	Calculates highest possible sum of cards.  This is to determine how to handle Ace cards in hands. 
	Arguments:
	- name: a string representing the name of player whose hand to check 
	Returns:
	- sum_hand: sum of the values of all cards in hand
	"""
	
	sum_hand = 0
	added_ace = False
	
	for card in players[name]['hand'][hand_num]:
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
	
	
def	sum_cards(name, hand_num=0):
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
	sum_hand = highest_sum_cards(name, hand_num)
	added_ace = has_ace(name, hand_num)

	#check for overage caused by Ace and adjust
	if sum_hand > 21:
		if added_ace:
			sum_hand -= 10
		
	return sum_hand
	
	
def check_21(name, hand_num=0):
	"""
	Checks whether the given player's hand has a value of 21.
	Arguments:
	- name: a string representing the person whose hand to check
	Returns:
	- True if value of hand is 21. False otherwise.
	"""
	
	return sum_cards(name, hand_num) == 21

	
def check_anyone_has_21():
	"""
	This check only happens at the beginning of each game - assumes looking at first hand only of each player.
	"""
	dealer_has_21 = check_21('dealer')
	player_has_21 = check_21('player')
	
	if dealer_has_21 or player_has_21:
		#single player - assuming game automatically over if one of them have 21, so show dealer hand
		#MP -- remove check from here, change status only.
		print_board(True)

	#	LINES MOVED TO CHECK_WINNER()
	
		if dealer_has_21 and player_has_21:
			print "Both of you have 21.  Draw."
			change_player_status('player','done')
		elif dealer_has_21:
	#		print "Sorry, dealer has 21.  You lose."
			change_player_status('player','loss')
	#		change_total_money('player', calculate_change('player','loss'))
		elif player_has_21:
	#		print "Player has Blackjack! You win!"
			change_player_status('player','done')
	#		change_total_money('player', calculate_change('player','blackjack'))
		return True
	else:
		return False

def has_ace(name, hand_num=0):
	"""
	Arguments:
	- name: a string representing the person whose hand to check
	Returns:
	- True if at least one Ace card exists in the hand. False otherwise.
	"""
	for card in players[name]['hand'][hand_num]:
		if 'A' in card:
			return True
			
	return False

def check_busted(name, hand_num=0):
	"""
	Checks if value of player's hand is greater than 21.
	Arguments:
	- name: a string representing the person whose hand to check
	Returns:
	- True if hand is greater than 21. False otherwise.
	"""
	
	return sum_cards(name, hand_num) > 21
		
def hit(name, used_cards, hand_num=0):
	"""
	Adds one card from the deck into a player's hand.
	Arguments:
	- name: a string representing player
	- used_cards: a list of indices representing cards already used in deck
	- hand: a list of cards representing the hand to add a card to
	Notes:
	- deal_cards() returns a list of one card - [0] is added to append the card itself to the hand
	"""
	
	players[name]['hand'][hand_num].append(deal_cards(1,used_cards)[0])

def deck_needs_shuffling(num_cards_used):
	"""
	Checks whether the deck needs to be shuffled based on current rule in rules['shuffle'].
	Arguments:
	- num_cards_used: an int representing the number of cards already used
	Returns:
	- True if the deck needs to be shuffled.  False otherwise.
	"""
	
	return num_cards_used > rules['shuffle']
	
def print_options(name, hand_num=0):
	"""
	Prints player's options.
	"""
	print "Choose from the following options:"
	print "    1 - Hit"
	print "    2 - Stand"
	if check_double(name, hand_num):
		print "    3 - Double"
	if check_split(name, hand_num):
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

def check_soft_17(name, hand_num=0):
	"""
	Check if a player's hand is a soft 17 (i.e. hand is 17 because A = 11)
	"""
	
	return highest_sum_cards(name, hand_num) == 17 and has_ace(name, hand_num)
		
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

def check_dealer_won(name, num):
	"""
	check if dealer won a given hand
	"""
	return sum_cards(name, num) < sum_cards('dealer') and not check_busted('dealer')
	
	
def check_winner():
	"""
	Checks who won the game. Currently only works for single player.
	"""
	print "----------------------"
	print " *** GAME RESULTS ***"
	print "----------------------\n"
	
	for num in range(len(players['player']['hand'])):
		print "PLAYER - HAND {}:".format(num+1)
		
		if check_busted('player', num):
			print "Busted! You lose."
			change_total_money('player', calculate_change('player','loss'))
		
		elif get_player_status('player', num) == 'loss':
			if check_21('dealer'):
				print "Sorry, dealer has 21.  You lose."
			else: 
				print "You lose."
			change_total_money('player', calculate_change('player','loss'))

		elif check_dealer_won('player', num):
			print "Sorry, dealer won."
			change_total_money('player', calculate_change('player', 'loss'))

		elif sum_cards('player', num) == sum_cards('dealer'):
			print "Push.\n"

		elif check_21('player') and len(players['player']['hand'][num]) == 2:
			print "Player has Blackjack! You win!"
			change_total_money('player', calculate_change('player','blackjack'))
			
		else:
			if check_busted('dealer'):				
				print "Dealer busted! Player wins!"
				
			elif sum_cards('player', num) > sum_cards('dealer'):
				print "Congratulations, player wins!"
				
			change_total_money('player', calculate_change('player', 'win'))

			
def change_player_status(name, status, hand_num=0):
	"""
	Change player's status
	"""
	players[name]['status'][hand_num] = status

	
def get_player_status(name, hand_num=0):
	return players[name]['status'][hand_num]

	
def reset_board():
	"""
	Reset the elements of the board for the next round.  Need to keep total money intact.
	"""
	for person in players:
		players[person]['hand'] = [[]]	
		players[person]['bet'] = [0]
		players[person]['status'] = ["playing"]

		
def process_hit(name, hand_num=0):
	"""
	Player has requested to hit.
	"""
	print "\n{} hits.".format(name.title())
	hit(name, used_cards_indices, hand_num)
	if check_busted(name, hand_num):
		print_board(True)  #changes for MP?
		change_player_status(name, 'loss', hand_num)
		
	elif check_21(name, hand_num):
		print_board(False)
		print "You have 21. Turn is over."
		change_player_status(name, 'done', hand_num)

		
def dealer_play():
	print "\nDealer's Turn\n"
	
	while get_player_status('dealer') == 'playing':
		if dealer_must_hit():
			hit('dealer', used_cards_indices)
		else:
			change_player_status('dealer', 'done')
	
	print_board(True)

	
def player_play(name, hand_num=0):
	"""
	Processes gameplay loop for a single player.
	"""
	
	while get_player_status(name, hand_num) == 'playing':
		print_board(False, hand_num)
		print "{}'s Turn - Hand {}\n".format(name.title(), hand_num+1)
		print_options(name, hand_num)
		move = raw_input("Enter the number for the move you want to make: ").strip()
		
		#if move is not valid, start loop over
		if not check_valid_move(move):
			continue
	
		if move == "1":
			process_hit('player', hand_num)
			
		elif move == "2":
			print "\nPlayer stands. Turn is over."
			change_player_status('player','done', hand_num) 
		
		elif move == "3":
			process_double('player', hand_num)
		
		elif move == "4":
			process_split('player', hand_num)
	


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
	
	#check if player has enough money, adds in $100 increments if not
	while not check_funding('player', rules['min_bet']):
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
		players[person]['hand'][0] = deal_cards(2,used_cards_indices)
				
	#check if anyone has 21
	check_anyone_has_21()
	
		
	#*** PLAYER GAME LOOP START ***
	
	#check if any player statuses are 'playing'
	while 'playing' in players['player']['status']:
		player_play('player', players['player']['status'].index('playing'))
			
	#*** DEALER GAME LOOP START ***		

	for status in players['player']['status']:
		if status != 'loss':
			dealer_play()
			break
	
	check_winner()				
	
		
#START GAME

def print_main_menu():
	print "Select from one of the following options:"
	print "    1: Play Blackjack"
	print "    2: Quit"
	print ""
	
def start_game():
	print "\nWELCOME TO BLACKJACK! \n"
	
	while True:
		print_main_menu()
		
		choice = raw_input("Enter choice selection: ").strip().lower()
		if choice == "1":
			print "Alright, let's play!\n"
			play_blackjack()
		elif choice == "2":
			print "Thanks for playing!"
			break 
		else:
			print "Sorry, I'm not sure what you mean by {}.\n".format(choice)
	
	

#TESTS

start_game()

def set_hand(name, card_list, hand_num=0):
	players[name]['hand'][hand_num] = card_list

#####################################################################
# Doctest code

# if __name__ == '__main__':
    # import doctest
    # if doctest.testmod().failed == 0:
        # print "\n*** ALL TESTS PASSED. AWESOME WORK!\n"
