# flake8: noqa

import random
from threading import Thread
from reach_rpc import mk_rpc


def main():
    rpc, rpc_callbacks = mk_rpc()
    player_1 = input("Player1 enter your name : ")
    player_2 = input("Player2 enter youe name : ")
    starting_balance = rpc("/stdlib/parseCurrency", 100)
    acc_alice = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob = rpc("/stdlib/newTestAccount", starting_balance)

    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))

    before_alice = get_balance(acc_alice)
    before_bob = get_balance(acc_bob)
    print("%s starting balance is %s algo" % (player_1, before_alice))
    print("%s starting balance is %s algo" % (player_2, before_bob))
    ctc_alice = rpc("/acc/contract", acc_alice)
    HAND = ["Rock", "Paper", "Scissors"]
    OUTCOME = [
        "Bob wins",
        "Draw",
        "Alice wins",
    ]
    Hands = {
        "Rock": 0,
        "R": 0,
        "r": 0,
        "Paper": 1,
        "P": 1,
        "p": 1,
        "Scissors": 2,
        "S": 2,
        "s": 2,
    }

    def player(who):
        def getHand():
            hand = input("%s select hand: " % (who))
            selected_hand = Hands[hand]
            if selected_hand == 0:
                print(
                    """%s played %s
     _______
----+   ____)
       (_____)
       (_____)
       (____)
-----+_(___)
                """
                    % (who, HAND[selected_hand])
                )

            elif selected_hand == 1:
                print(
                    """%s played %s
     _____
----+   ___)___
       ________)__
       ___________)
       __________)
-----+________)
                """
                    % (who, HAND[selected_hand])
                )

            elif selected_hand == 2:
                print(
                    """%s played %s
     _____
----+   ___)___
       _________)__
       ____________)
       (____)
-----+_(___)
                """
                    % (who, HAND[selected_hand])
                )
            return selected_hand

        def informTimeout():
            print("%s observed a timeout" % who)

        def seeOutcome(n):
            print(
                "%s saw outcome %s"
                % (who, OUTCOME[rpc("/stdlib/bigNumberToNumber", n)])
            )

        return {
            "stdlib.hasRandom": True,
            "getHand": getHand,
            "informTimeout": informTimeout,
            "seeOutcome": seeOutcome,
        }

    def play_alice():
        num = int(input("%s how much will u like to wager: " % (player_1)))
        rpc_callbacks(
            "/backend/Alice",
            ctc_alice,
            dict(
                wager=rpc("/stdlib/parseCurrency", num), deadline=10, **player(player_1)
            ),
        )

    alice = Thread(target=play_alice)
    alice.start()

    def play_bob():
        ans = input(
            "%s would u like to accept the wager\nReply with y/n: " % (player_2)
        )
        if ans == "y":

            def acceptWager(amt):
                print("%s accepts the wager of %s" % (player_2, fmt(amt)))

            ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
            rpc_callbacks(
                "/backend/Bob",
                ctc_bob,
                dict(acceptWager=acceptWager, **player(player_2)),
            )
            rpc("/forget/ctc", ctc_bob)
        elif ans == "n":
            print("wager not accepted")
            quit()

    bob = Thread(target=play_bob)
    bob.start()

    alice.join()
    bob.join()

    after_alice = get_balance(acc_alice)
    after_bob = get_balance(acc_bob)

    print("%s went from %s to %s" % (player_1, before_alice, after_alice))
    print("%s went from %s to %s" % (player_2, before_bob, after_bob))

    rpc("/forget/acc", acc_alice, acc_bob)
    rpc("/forget/ctc", ctc_alice)


if __name__ == "__main__":
    main()
