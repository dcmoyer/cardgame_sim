#!/usr/bin/python
#
#   This is a "War" Card Game simulator to answer Dan Lander's Question.
#
#   It will simulate a large number of games and
#   return the observed distribution of stopping
#   times.
#
#   DMoyer 011914
#
#   0830 011914 Created.

import random
from collections import deque
import numpy as np
from matplotlib import pyplot as plt

random.seed('UCLA')

deck = list()
for x in range(13):
    for i in range(4):
        deck.append(x)

def war_sim():
    
    count = 0
    
    random.shuffle(deck)
    p1_deck = deque()
    for x in deck[:26]:
        p1_deck.append(x)
    p2_deck = deque()
    for x in deck[26:]:
        p2_deck.append(x)
    p1_facedown = deque()
    p2_facedown = deque()
    
    #TOP OF DECK IS "LEFT"
    while(len(p1_deck) != 0 and len(p2_deck) != 0):
        #if(count > 100):
        #    break
        count = count + 1
        p1_card = p1_deck.popleft()
        p2_card = p2_deck.popleft()
        
        #winner first takes opponent card
        #then takes their own
        if(p1_card > p2_card): #player 1 wins!
            p1_deck.append(p2_card)
            p1_deck.append(p1_card)
        elif(p1_card < p2_card): #player 2 wins!
            p2_deck.append(p1_card)
            p2_deck.append(p2_card)
        else: #tie
            while(p1_card == p2_card):
                p1_facedown.append(p1_card)
                p2_facedown.append(p2_card)
                try:
                    for i in range(3):
                        p1_facedown.append(p1_deck.popleft())
                        p2_facedown.append(p2_deck.popleft())
                    p1_card = p1_deck.popleft()
                    p2_card = p2_deck.popleft()
                except IndexError, TypeError:
                    return count
                
                #Player takes opponents cards in reverse order of play,
                #then takes their own in reverse order of play.
                if(p1_card > p2_card): #player 1 wins!
                    p1_deck.append(p2_card)
                    while(len(p2_facedown) != 0):
                        p1_deck.append(p2_facedown.pop())
                    p1_deck.append(p1_card)
                    while(len(p1_facedown) != 0):
                        p1_deck.append(p1_facedown.pop())
                    break
                elif(p1_card < p2_card): #player 2 wins!
                    p2_deck.append(p1_card)
                    while(len(p1_facedown) != 0):
                        p2_deck.append(p1_facedown.pop())
                    p2_deck.append(p2_card)
                    while(len(p2_facedown) != 0):
                        p2_deck.append(p2_facedown.pop())
                    break
                #end if
            #end whi;e
        #endif
    #endwhile
    return count
#end

def test(iter = 20000):
    output = np.array([0 for x in range(iter)])
    for i in range(iter):
        output[i] = war_sim()
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(2,1,1)
    ax2 = fig1.add_subplot(2,1,2)
    ax1.hist(np.log(output), bins = 200)
    ax2.hist(output, bins = 200)
    plt.show()

if __name__ == '__main__':
    test()