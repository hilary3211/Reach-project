# flake8: noqa

import random
from threading import Thread  # importing required libs
from reach_rpc import mk_rpc


def main():
    rpc, rpc_callbacks = mk_rpc()
    starting_balance = rpc(
        "/stdlib/parseCurrency", 10
    )  # allocate a certain amount of tokens
    acc_alice = rpc(
        "/stdlib/newTestAccount", starting_balance
    )  # creating accounts for Alice player 1
    acc_bob = rpc(
        "/stdlib/newTestAccount", starting_balance
    )  # creating accounts for bob player 2

    def fmt(x):
        return rpc(
            "/stdlib/formatCurrency", x, 4
        )  # create a fuctio that formats to 4 decimal place

    def get_balance(w):
        return fmt(
            rpc("/stdlib/balanceOf", w)
        )  # creating a function that retrieves the balance of a player in a formatted form

    before_alice = get_balance(
        acc_alice
    )  # getting the balace of alice before she starts playing the game
    before_bob = get_balance(
        acc_bob
    )  # getting the balance of bob before he starts playing the game
    print("Alice starting balance is " + str(before_alice) + " algo")
    print("Bob's starting balance is " + str(before_bob)+ " algo")
    ctc_alice = rpc("/acc/contract", acc_alice)  # deploying alice contract
    HAND = ["Rock", "Paper", "Scissors"]  # creating the hand parameters
    OUTCOME = [
        "Bob wins",
        "Draw",
        "Alice wins",
    ]  # creating a var for the outcome parameters

    def player(who):  # creating a fuction that will enable a user play
        
        def getHand():  # creating function to get the hand of the player at random
            hand = random.randint(0, 2)
            if hand == 0:
                print("""%s played %s
     _______
----+   ____)
       (_____)
       (_____)
       (____)
-----+_(___)
                """ % (who, HAND[hand])) 

            elif hand == 1:
                print("""%s played %s
     _____
----+   ___)___
       ________)__
       ___________)
       __________)
-----+________)
                """ % (who, HAND[hand])) 

            elif hand == 2:
                print("""%s played %s
     _____
----+   ___)___
       _________)__
       ____________)
       (____)
-----+_(___)
                """ % (who, HAND[hand]))
            return hand

        def informTimeout():  # creating a function that puts a little bit of timeout
            print("%s observed a timeout" % who)

        def seeOutcome(n):  # function that shows the outcome of the game
            print(
                "%s saw outcome %s"
                % (who, OUTCOME[rpc("/stdlib/bigNumberToNumber", n)])
            )

        return {
            "stdlib.hasRandom": True,
            "getHand": getHand,  # returns a dict that contains this information
            "informTimeout": informTimeout,
            "seeOutcome": seeOutcome,
        }

    def play_alice():  # this uses all the code we wrote above to play for alice
        rpc_callbacks(
            "/backend/Alice",
            ctc_alice,
            dict(wager=rpc("/stdlib/parseCurrency", 5), deadline=10, **player("Alice")),
        )  # the rpc_callbacks helps all its parameters interact with the server

    alice = Thread(target=play_alice)
    alice.start()  # enables alice play

    def play_bob():  # create function that enables bob play
        def acceptWager(amt):
            print("Bob accepts the wager of %s" % fmt(amt))

        ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
        rpc_callbacks(
            "/backend/Bob", ctc_bob, dict(acceptWager=acceptWager, **player("Bob"))
        )
        rpc("/forget/ctc", ctc_bob)

    bob = Thread(target=play_bob)
    bob.start()  # enables bob play

    alice.join()  # instructs the main thread to wait until both child threads have run to completion, signifying the end of the Rock, Paper, Scissors! game
    bob.join()

    after_alice = get_balance(acc_alice)  # gets the current balance of alice
    after_bob = get_balance(acc_bob)  # gets the current balance of bob

    print("Alice went from %s to %s" % (before_alice, after_alice))
    print("Bob went from %s to %s" % (before_bob, after_bob))

    rpc(
        "/forget/acc", acc_alice, acc_bob
    )  # release Alice and Bob's RPC handles from the server's memory
    rpc("/forget/ctc", ctc_alice)


if __name__ == "__main__":
    main()