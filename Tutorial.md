<p align="center">
  <a href="" rel="noopener">
 <img src="https://docs.reach.sh/assets/logo.png" alt="Project logo"></a>
</p>
<h3 align="center">Loopable Rock, Paper, Scissors</h3>

<div align="center">


</div>

---

<p align="center"> Tutorial for the Loopale rock,paper,scissors
    <br> 
</p>

This tutorial assumes you have completed the Rock,Paper,Scissor tutorial on the reach docs 

This tutorial explains step by step how the loopable rock, paper, scissors works from ground up, so get ready!!!

```
'reach 0.1';
const [isHand, ROCK, PAPER, SCISSORS] = makeEnum(3)

const [isOutcome, B_WINS, DRAW, A_WINS] = makeEnum(3) 

const winner = (handA, handB) => ((handA + (4 - handB)) % 3)


assert(winner(ROCK, PAPER) == B_WINS)
assert(winner(PAPER, ROCK) == A_WINS)
assert(winner(ROCK, ROCK) == DRAW)

forall(UInt, handA =>
    forall(UInt, handB =>
        assert(isOutcome(winner(handA, handB)))))

forall(UInt, (hand) =>
    assert(winner(hand, hand) == DRAW))
```

* As you know Line 1 is used to specify the version of reach 
* From line 2 to 6 we create functions and variables we use within the program
* From line 9 to 18 ensures that all the the functions work using the assert function

Now lets dive into creating the participant of the game Alice and Bob.  The first step is to create the functions which will be used by both participant frontend to communicate with the reach backend code. 

```
const Player = { 
    ...hasRandom,
    getHand: Fun([], UInt), 
    getHand1: Fun([], UInt), 
    getHand2: Fun([], UInt),
    seeOutcome: Fun([UInt], Null),
    informTimeout: Fun([], Null)
};

export const main = Reach.App(() => {
    const Alice = Participant('Alice', {
        ...Player,
        wager: UInt,
        deadline: UInt
    });
    const Bob = Participant('Bob', {
        ...Player,
        acceptWager: Fun([UInt], Null),
    });

    init();
```
* Line 20 to Line 27 defines the functions the two participants have in common. These functions are all stored in a variable name called Player 
* Line 29 to Line 38 creates the participants of the game and includes their functions

* Line 40 is used to initalize the creation participants

Now create a new file and name it index.py, this file will contain the frontend code. Let's dive right into it below

```
# flake8: noqa
from threading import Thread
from reach_rpc import mk_rpc
import time
def main():
    rpc, rpc_callbacks = mk_rpc()

    starting_balance = rpc("/stdlib/parseCurrency", 100)
    player_1 = input("Enter your name player1: ")
    player_2 =input("Enter your name player2: ")
    acc_alice = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob = rpc("/stdlib/newTestAccount", starting_balance)

    

    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))

    before_alice = get_balance(acc_alice)
    before_bob = get_balance(acc_bob)

    print("%s starting balance is %s algo" %(player_1,before_alice))
    print("%s starting balance is %s algo"%(player_2,before_bob))

    ctc_alice = rpc("/acc/contract", acc_alice)

    OUTCOME = [
        "%s wins" %(player_2),
        "Draw",
        "%s wins"%(player_1),
    ]
    HAND = ["Rock", "Paper", "Scissors"]
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


```
* From line 2 to line 4 we are simply importing modules we will use in the frontend code, like the rpc server which will be used to connect our frontend python code to the reach backend code.

* On line 6 the Python program binds rpc and rpc_callbacks out of mk_rpc. These two functions are the only tools we will need to communicate with the RPC server.
* From line 8 to line 12 we are simply creating test account, account names of the players and funding those accounts 
* From line 16 to line 20 we create two functions, the fmt function is used to format the account balance to 4 decimal places, while the getbalance function is used to the balance of the test accounts used in the game
* From line 22 to line 26 we are simply trying to get the balance to the account before the game begins and print it out  
* On Line 28 we are deploying the contract 
* From line 30 to line 46 we create a dictionary ad lists used within the program 

So now we are going to create the functions, using the the same function names we used in the reach backend code above 

```
def player(who):
        def getHand():
            time.sleep(5)
            if who == player_1:
                hand = input("Enter your hand player1: ")
            elif who == player_2:
                hand = input("Enter your hand player2: ")
            selected_hand = Hands[hand]
            return selected_hand
        
        def getHand1():
            time.sleep(5)
            if who == player_1:
                hand = input("Enter your hand player1: ")
            elif who == player_2:
                hand = input("Enter your hand player2: ")
            selected_hand = Hands[hand]
            return selected_hand

        def getHand2():
            time.sleep(5)
            if who == player_1:
                hand = input("Enter your hand player1: ")
            elif who == player_2:
                hand = input("Enter your hand player2: ")
            selected_hand = Hands[hand]
            return selected_hand
        
        def informTimeout():
            print("%s observed a timeout" % who)

        def seeOutcome(n):
            print(
                "%s saw outcome %s this round"
                % (who, OUTCOME[rpc("/stdlib/bigNumberToNumber", n)])
            )

        return {
            "stdlib.hasRandom": True,
            "getHand": getHand,
            "getHand1": getHand1,
            "getHand2": getHand2,
            "informTimeout": informTimeout,
            "seeOutcome": seeOutcome,
        }
```
* On line 48 we create the general player function with the player name argument. This main player function contains sub functions which has all the functionality the players in the game posses 
* Line 49 to Line 56 contains the first gethand function which is used to get the hands of the users in the first round of the game.
* Line 58 to Line 65 contains the second gethand function which is used to get the hands of the two players in the second round of the game.
* Line 67 to line 74 contains the third gethand function which is used to get the hands of the two players in third round of the game 
* Line 76 to line 77 contains the function built to help inform timeouts in game 
* Line 78 to line 83 contains a function that is used in the program to see the outcome each round 
* On line 85 to line 91 we simply return this subfunctions of the main player function.
Now we are done creating the functions on the frontend, we are going to implement them on the backend.
```
    Alice.only(() => {
        const wager = declassify(interact.wager)
    })

    Alice.publish(wager)
        .pay(wager)
    commit()


    Bob.only(() => {
        interact.acceptWager(wager)
    })
    Bob.pay(wager)
    commit()
    Alice.only(() => {
        const _handAlice = interact.getHand()
        const [_commitAlice, _saltAlice] = makeCommitment(interact, _handAlice)
        const commitAlice = declassify(_commitAlice)
    })
    Alice.publish(commitAlice)
    commit()

    unknowable(Bob, Alice(_handAlice, _saltAlice))

    Bob.only(() => {
        const handBob = declassify(interact.getHand())
    })
    Bob.publish(handBob)
    commit()

    Alice.only(() => {
        const saltAlice = declassify(_saltAlice)
        const handAlice = declassify(_handAlice)
    })

    Alice.publish(saltAlice, handAlice)

    checkCommitment(commitAlice, saltAlice, handAlice)
    const outcome = winner(handAlice, handBob)
    each([Alice, Bob], () => {
        interact.seeOutcome(outcome)
    })
    commit()
```
In this index.rsh file above we use some of the fuctions we defined in the index.py frontend code. We use the gethand function to get the hands of both players for the first round and also we use the seeOutcome function to see the outcome of the first round. 
* In line 56 to line 84 we are using to gethand function to get the players hand, then we make a commitment to hide the first players hand till the second player reveals their hands 

The code below does exactly the same as the one above but it uses the gethand1 and gethand2 function to get the players hands for the second round and the last round. Towards the end of the index.rsh we use a computation to determine the winner of the 3 rounds and transfer the funds in the contract to winner , or in the case of a draw the funds will be transfered back to the two players.
```
Alice.only(() => {
        const _handAlice2 = interact.getHand1()
        const [_commitAlice2, _saltAlice2] = makeCommitment(interact, _handAlice2)
        const commitAlice2 = declassify(_commitAlice2)
    })
    Alice.publish(commitAlice2)
    commit()


    unknowable(Bob, Alice(_handAlice2, _saltAlice2))
    Bob.only(() => {
        const handBob2 = declassify(interact.getHand1())
    })
    Bob.publish(handBob2)
    commit()

    Alice.only(() => {
        const saltAlice2 = declassify(_saltAlice2)
        const handAlice2 = declassify(_handAlice2)
    })

    Alice.publish(saltAlice2, handAlice2)
    checkCommitment(commitAlice2, saltAlice2, handAlice2)


    const outcome2 = winner(handAlice2, handBob2)
    each([Alice, Bob], () => {
        interact.seeOutcome(outcome2) 
    })
    commit()

     Alice.only(() => {
        const _handAlice3 = interact.getHand2()
        const [_commitAlice3, _saltAlice3] = makeCommitment(interact, _handAlice3)
        const commitAlice3 = declassify(_commitAlice3)
    })
    Alice.publish(commitAlice3)
    commit()


    unknowable(Bob, Alice(_handAlice3, _saltAlice3))
    Bob.only(() => {
        const handBob3 = declassify(interact.getHand2())
    })
    Bob.publish(handBob3)//publishing the hand 
    commit()

    Alice.only(() => {
        const saltAlice3 = declassify(_saltAlice3)
        const handAlice3 = declassify(_handAlice3)
    })

    Alice.publish(saltAlice3, handAlice3)
    checkCommitment(commitAlice3, saltAlice3, handAlice3)


    const outcome3 = winner(handAlice3, handBob3)

    const [forAlice, forBob] =
        outcome2 == A_WINS && outcome == A_WINS || outcome == A_WINS && outcome3 == A_WINS || outcome2 == A_WINS && outcome3 == A_WINS ? [2, 0] :
            outcome2 == B_WINS && outcome == B_WINS || outcome == B_WINS && outcome3 == B_WINS || outcome2 == B_WINS && outcome3 == B_WINS ? [0, 2] :
                [1, 1] /* tie */

    transfer(forAlice * wager).to(Alice)
    transfer(forBob * wager).to(Bob)
    commit();


    each([Alice, Bob], () => {
        interact.seeOutcome(outcome3)
    })
})
```
Now lets see how all this is implemented in the frontend code

```
 def play_alice():
        num = input("Enter your wager player1: ")
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
        wag =input("Do you accept wager player2: ")
        if wag == "yes" or wag == "y" or wag == "Y" or wag == "YES":

            def acceptWager(amt):
                print("%s accepts the wager of %s" % (player_2, fmt(amt)))

            ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
            rpc_callbacks(
                "/backend/Bob",
                ctc_bob,
                dict(acceptWager=acceptWager, **player(player_2)),
            )
            rpc("/forget/ctc", ctc_bob)
        elif wag == "n" or wag == "no" or wag == "NO" or wag == "N":
            print("wager not accepted")
            quit()

    bob = Thread(target=play_bob)
    bob.start()

    alice.join()
    bob.join()

    after_alice = get_balance(acc_alice)
    after_bob = get_balance(acc_bob)

    print("%s went from %s to %s" % (player_1,before_alice, after_alice))
    print("%s went from %s to %s" % (player_2,before_bob, after_bob))

    rpc("/forget/acc", acc_alice, acc_bob)
    rpc("/forget/ctc", ctc_alice)


if __name__ == "__main__":
    main()

```
* From line 93 to line 101 we create a function play_alice(), this function will be used to execute player1( which is alice) functions in the game, this is done on line 103 and 104 using the thread function
* From line 106 to line 121 we also a create a function play_bob(), this is used to execute player2 functionalities in the game. we also use the thread function to execute the function on line 123 and line 124. 
* On line 126 and 127 we use the .join() to instructs the main thread to wait until both child threads have run to completion, signifying the end of the game.
 
Towards the ending of the code we just get the balance of the two accounts and print it on the terminal, then we forget the contract just in case the users want to play again.

Below is the full game output on the terminal 
```
Enter your name player1: Alice
Enter your name player2: Bob     
Alice starting balance is 100 algo
Bob starting balance is 100 algo
Enter your wager player1: 30
Do you accept wager player2: y
Bob accepts the wager of 30
Enter your hand player1: r
Enter your hand player2: s
Alice saw outcome Alice wins this round
Bob saw outcome Alice wins this round
Enter your hand player1: s
Enter your hand player2: r
Alice saw outcome Bob wins this round
Bob saw outcome Bob wins this round
Enter your hand player1: p
Enter your hand player2: p
Alice saw outcome Draw this round
Bob saw outcome Draw this round
Alice went from 100 to 99.987
Bob went from 100 to 99.9951
```
