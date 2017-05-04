deck = [('A','H'),(2,'H'),(3,'H'),(4,'H'),(5,'H'),(6,'H'),(7,'H'),(8,'H'),(9,'H'),(10,'H'),('J','H'),('Q','H'),('K','H'),
('A','D'),(2,'D'),(3,'D'),(4,'D'),(5,'D'),(6,'D'),(7,'D'),(8,'D'),(9,'D'),(10,'D'),('J','D'),('Q','D'),('K','D'),
('A','C'),(2,'C'),(3,'C'),(4,'C'),(5,'C'),(6,'C'),(7,'C'),(8,'C'),(9,'C'),(10,'C'),('J','C'),('Q','C'),('K','C'),
('A','S'),(2,'S'),(3,'S'),(4,'S'),(5,'S'),(6,'S'),(7,'S'),(8,'S'),(9,'S'),(10,'S'),('J','S'),('Q','S'),('K','S')]

used_cards = []

hands_dict = {dealer: [], player: []}


[fn] shuffle deck
	clear list of already used cards

[fn] deal_cards (num_cards)
	cards = []
	for number of cards needed:
		generate random number between 0-51
		check if number has already been used during this shuffle
			if yes, generate another number
			if no, 
				add number to already used list
				add corresponding card to cards list
	return cards
	
	
[fn] print_board (all_hands, show_dealer_hand)
	show_dealer_hand: if True, then show all cards in dealer hand.  if False, only show one card (assumes only 2 cards if no).
	print "DEALER:"
		if show_dealer_hand = yes:
			print '[]' + dealer[1]  
			else:
			for all cards in deck
				print card
	
	print "PLAYER:"
		for all cards in deck
			print card
	
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


code outline:

[fn] main function to start blackjack game

	[fn] shuffle deck if needed
	[fn] deal cards
	[fn] print game board -- showing player's 2 cards and dealer's 2nd card only
	[fn] check if player has 21 to start 
			- if yes, automatic win
			- if no, continue
	
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
