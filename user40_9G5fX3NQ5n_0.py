import random

#Function that changes the name input to numbers
def name_to_number(name):
    if str.lower(name) == "rock":
        name = 0
        return name
    elif str.lower(name) == "spock":
        name = 1
        return name
    elif str.lower(name) == "paper":
        name = 2
        return name
    elif str.lower(name) == "lizard":
        name = 3
        return name
    elif str.lower(name) == "scissors":
        name = 4
        return name
    else:
        print "Invalid input. Try again"

#Function that changes the number input to names
def number_to_name(number):
    if number == 0:
        name = "rock"
        return name
    elif number == 1:
        name = "Spock"
        return name
    elif number == 2:
        name = "paper"
        return name
    elif number == 3:
        name = "lizard"
        return name
    elif number == 4:
        name = "scissors"
        return name
    else:
        print "Invalid input. Try again"
        
#main function for RPSLS
def rpsls(player_choice):
    print
    print "Player chooses", player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses", comp_choice
#test condition to check who wins
    if (comp_number - player_number) % 5 == 1 or (comp_number - player_number) % 5 == 2:
        print "Computer wins!"
    elif (comp_number - player_number) % 5 == 3 or (comp_number - player_number) % 5 == 4:
        print "Player wins!"
    elif comp_number == player_number:
        print "Player ande computer tie!"
#test
print rpsls("rock")
print rpsls("Spock")
print rpsls("paper")
print rpsls("lizard")
print rpsls("scissors")