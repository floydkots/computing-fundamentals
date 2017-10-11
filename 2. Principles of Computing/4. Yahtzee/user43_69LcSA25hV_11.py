"""
Author: Floyd Kots ~ github.com/floydkots
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set
    
def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    return max([(hand.count(dice) * dice) for dice in hand])

def sorted_seqs(seqs):
    """
    Return the list of sequences with the sequences sorted
    """
    return [tuple(sorted(seq)) for seq in seqs]
    
    
def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    all_free_rolls = gen_all_sequences(range(1, num_die_sides + 1),
                                       num_free_dice) 
    total_score = 0
    for roll in all_free_rolls:
        my_score = score(held_dice + roll)
        total_score += my_score

    return float(total_score) / len(all_free_rolls)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set([()])
    for _ in range(len(hand)):
        for hold in set(all_holds):
            for die in hand:
                new_hold = list(hold)
                if not new_hold or die not in new_hold or hand.count(die) > new_hold.count(die):
                    new_hold.append(die)
                all_holds.add(tuple(sorted(new_hold)))
    return all_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """   
    all_holds = gen_all_holds(hand)
    holds = []
    for hold in all_holds:
        value = expected_value(hold, num_die_sides, len(hand) - len(hold))
        holds.append((value, hold))    
    return max(holds)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (2, 5, 1, 5, 2)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

#Uncomment for further tests
#from user43_g9qJbIPVZfI2bwB_9 import test_yahtzee    
#test_yahtzee(score, expected_value, gen_all_holds, strategy)


    



