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

The logic we are trying to implement is loopable rock,paper,scissors.It is variant of rock, paper, scissors in which moves are submitted in batches (to keep transaction costs low) and the first move alternates between two players.
So we are going to have two participant an attacher and a deployer or Player1 and Player2.
The aim of this tutorial explains step by step on how the loopable rock, paper, scissors program works from ground up.
For this Tutorial we are creating a console application using python, so get readyyy!!!

```js
1 'reach 0.1'
2 const [isOutcome, B_WINS, DRAW, A_WINS] = makeEnum(3)
3 
4 const winner = (handA, handB) => ((handA + (4 - handB)) % 3)
5 
6 assert(winner(ROCK, PAPER) == B_WINS)
7 assert(winner(PAPER, ROCK) == A_WINS)
8 assert(winner(ROCK, ROCK) == DRAW)
9
10 forall(UInt, handA =>
11    forall(UInt, handB =>
12       assert(isOutcome(winner(handA, handB)))))
13
14 forall(UInt, (hand) =>
15    assert(winner(hand, hand) == DRAW))
```

* Line 1 is used to specify the version of [REACH](https://docs.reach.sh/tut/rps/#tut)
* From line 2 to 4 we create functions and variables we use within the program
* From line 6 to 15 ensures that all the the functions work using the assert function

Now let's dive into creating the participant of the game Alice and Bob.  The first step is to create the functions which will be used by both participant frontend to communicate with the REACH backend code. 

```js
16 const Player = { 
17    ...hasRandom,
18    getHand: Fun([], UInt), 
19    getHand1: Fun([], UInt), 
22    getHand2: Fun([], UInt),
21    seeOutcome: Fun([UInt], Null),
22    informTimeout: Fun([], Null)
23 }
```
* Line 16 to Line 23 defines the functions the two participants have in common. These functions are all stored in a variable name called Player
```js
24 export const main = Reach.App(() => {
25    const Alice = Participant('Alice', {
26        ...Player,
27        wager: UInt,
28        deadline: UInt
29    })
30    const Bob = Participant('Bob', {
31        ...Player,
32        acceptWager: Fun([UInt], Null),
33    })
34
35    init()
```
* Line 24 to Line 33 creates the participants of the game and includes their functions
* Line 35 is used to initalize the REACH application

Now create a new file and name it index.py, this file will contain the frontend code. Let's dive right into it below

```py
1 # flake8: noqa
2 from threading import Thread
3 from reach_rpc import mk_rpc
4 import time
5 def main():
6     rpc, rpc_callbacks = mk_rpc()
7
8     starting_balance = rpc("/stdlib/parseCurrency", 100)
9     player_1 = input("Enter your name player1: ")
10    player_2 =input("Enter your name player2: ")
11    acc_alice = rpc("/stdlib/newTestAccount", starting_balance)
12    acc_bob = rpc("/stdlib/newTestAccount", starting_balance)
```
* From line 2 to line 4 we are importing modules we will use in the frontend code, like the rpc server which will be used to connect our frontend python code to the REACH backend code.
* On line 6 the Python program binds rpc and rpc_callbacks out of mk_rpc. These two functions are the only tools we will need to communicate with the RPC server.
* From line 8 to line 12 we are creating test account, account names of the players and funding those accounts 

```py
13    def fmt(x):
14        return rpc("/stdlib/formatCurrency", x, 4)
15
16    def get_balance(w):
17        return fmt(rpc("/stdlib/balanceOf", w))
18
19    before_alice = get_balance(acc_alice)
20    before_bob = get_balance(acc_bob)
21
22    print("%s starting balance is %s algo" %(player_1,before_alice))
23    print("%s starting balance is %s algo"%(player_2,before_bob))
24
25    ctc_alice = rpc("/acc/contract", acc_alice)
26
27    OUTCOME = [
28        "%s wins" %(player_2),
29        "Draw",
30        "%s wins"%(player_1),
31    ]
32    HAND = ["Rock", "Paper", "Scissors"]
33    Hands = {
34        "Rock": 0,
35        "R": 0,
36        "r": 0,
37        "Paper": 1,
38        "P": 1,
39        "p": 1,
40        "Scissors": 2,
41        "S": 2,
42        "s": 2,
43    }
```

* From line 13 to line 17 we create two functions, the fmt function is used to format the account balance to 4 decimal places, while the getbalance function is used to get the balance of the test accounts used in the game.
* From line 19 to line 23 we are trying to get the balance to the account before the game begins and print it out.  
* On Line 25 we deploy the contract 
* From line 27 to line 43 we create a dictionary and list to store some information used within the program.

So now we are going to create the functions, using the the same function names we used in the REACH backend code above 

```py
36 def player(who):
37        def getHand():
38            time.sleep(5)
39            if who == player_1:
40                hand = input("Enter your hand player1: ")
41            elif who == player_2:
42                hand = input("Enter your hand player2: ")
52            selected_hand = Hands[hand]
53            return selected_hand
54        
55        def getHand1():
56            time.sleep(5)
57            if who == player_1:
58                hand = input("Enter your hand player1: ")
59            elif who == player_2:
60                hand = input("Enter your hand player2: ")
61            selected_hand = Hands[hand]
62            return selected_hand
63
64        def getHand2():
65            time.sleep(5)
66            if who == player_1:
67                hand = input("Enter your hand player1: ")
68            elif who == player_2:
69                hand = input("Enter your hand player2: ")
70            selected_hand = Hands[hand]
71            return selected_hand
```
* On line 45 we create the general player function with the player name as an argument of the function. This main player function contains sub functions which has all the functionality the players in the game posses 
* Line 46 to Line 53 contains the first gethand function which is used to get the hands of the users in the first round of the game.
* Line 55 to Line 62 contains the second gethand function which is used to get the hands of the two players in the second round of the game.
* Line 64 to line 71 contains the third gethand function which is used to get the hands of the two players in third round of the game 
```py       
72        def informTimeout():
73            print("%s observed a timeout" % who)
74
75        def seeOutcome(n):
76            print(
77                "%s saw outcome %s this round"
78                % (who, OUTCOME[rpc("/stdlib/bigNumberToNumber", n)])
79            )
80
81        return {
82            "stdlib.hasRandom": True,
83            "getHand": getHand,
84            "getHand1": getHand1,
85            "getHand2": getHand2,
86            "informTimeout": informTimeout,
87            "seeOutcome": seeOutcome,
88        }
```
Keep in mind this functions listed above are still part of the player function
* Line 72 to line 73 contains the function built to help inform timeouts in game 
* Line 75 to line 79 contains a function that is used in the program to see the outcome each round 
* On line 81 to line 88 we return this subfunctions of the main player function.
Now we are done creating the functions on the frontend, we are going to implement them on the backend.
```js
42    Alice.only(() => {
43        const wager = declassify(interact.wager)
44    })
45
46    Alice.publish(wager)
47        .pay(wager)
48    commit()
49
50
51    Bob.only(() => {
52        interact.acceptWager(wager)
53    })
54    Bob.pay(wager)
55    commit()
```
* On Line 42 to 48 we use one of Alice's function to declare the wager for the game, Alice publishes and pays this wager on line 46 and 47.
* From Line 51 to 55 we equally use one of Bob's function to accept the wager proposed by Alice,publish this wager,pay and commit 
```js
56    Alice.only(() => {
57        const _handAlice = interact.getHand()
58        const [_commitAlice, _saltAlice] = makeCommitment(interact, _handAlice)
59        const commitAlice = declassify(_commitAlice)
60    })
61    Alice.publish(commitAlice)
62    commit()
63
64    unknowable(Bob, Alice(_handAlice, _saltAlice))
65
66    Bob.only(() => {
67        const handBob = declassify(interact.getHand())
68    })
69    Bob.publish(handBob)
70    commit()
71
72    Alice.only(() => {
73        const saltAlice = declassify(_saltAlice)
74        const handAlice = declassify(_handAlice)
75    })
76
77    Alice.publish(saltAlice, handAlice)
78    checkCommitment(commitAlice, saltAlice, handAlice)
79    const outcome = winner(handAlice, handBob)
80    each([Alice, Bob], () => {
91        interact.seeOutcome(outcome)
82    })
83    commit()
```
In this index.rsh file above we use some of the fuctions we defined in the index.py frontend code. We use the gethand function to get the hands of both players for the first round and also we use the seeOutcome function to see the outcome of the first round. 
* From Line 56 to 60 we use the gethand function to get the hand alice plays for the first round, we then make a commitment to hide the hand until the second player publishes their hand.
* On line 61 and 62 we publish this commitment and commit.
* On Line 64 we use the unknowable function to ensure that Bob doesn't know Alice hand.
* From line 66 to 68 we use the gethand function to get Bob's hand for the first round of the game, then we publish and commit on line 69 and 70.
* From line 72 to 77 we reveal Alice hand and publish it for everyone to see.
* On line 78 we use the checkCommitment function to ensure the commitment published above by alice wasn't tampered with
* From Line 79 to 83 we get the outcome using the winner function we created earlier, then we use the seeoutcome function to display the outcome to both participants and commit.

The code below does exactly the same as the one above but it uses the gethand1 and gethand2 function to get the players hands for the second round and the last round. Towards the end of the index.rsh we use a computation to determine the winner of the 3 rounds and transfer the funds in the contract to winner, or in the case of a draw the funds will be transfered back to the two players.
```js
84 Alice.only(() => {
85        const _handAlice2 = interact.getHand1()
86        const [_commitAlice2, _saltAlice2] = makeCommitment(interact, _handAlice2)
87        const commitAlice2 = declassify(_commitAlice2)
88    })
89    Alice.publish(commitAlice2)
90    commit()
100
101    unknowable(Bob, Alice(_handAlice2, _saltAlice2))
102    Bob.only(() => {
103        const handBob2 = declassify(interact.getHand1())
104    })
105    Bob.publish(handBob2)
106    commit()
107
108    Alice.only(() => {
109        const saltAlice2 = declassify(_saltAlice2)
110        const handAlice2 = declassify(_handAlice2)
111    })
112
113    Alice.publish(saltAlice2, handAlice2)
114    checkCommitment(commitAlice2, saltAlice2, handAlice2)
115
116    const outcome2 = winner(handAlice2, handBob2)
117    each([Alice, Bob], () => {
118        interact.seeOutcome(outcome2) 
119    })
120    commit()
```
* From Line 84 to 88 we use the gethand1 function to get the hand alice plays for the second round, we then make a commitment to hide the hand until the second player publishes their hand.
* On line 89 and 90 we publish this commitment and commit.
* On Line 101 we use the unknowable function to ensure that Bob doesn't know Alice hand.
* From line 102 to 104 we use the gethand1 function to get Bob's hand for the second round of the game, then we publish and commit on line 105 and 106.
* From line 108 to 113 we reveal Alice hand and publish it for everyone to see.
* On line 114 we use the checkCommitment function to ensure the commitment published above by alice wasn't tampered with
* From Line 116 to 120 we get the outcome using the winner function we created earlier, then we use the seeoutcome function to display the outcome to both participants and commit.
```js
121
122     Alice.only(() => {
123        const _handAlice3 = interact.getHand2()
124        const [_commitAlice3, _saltAlice3] = makeCommitment(interact, _handAlice3)
125        const commitAlice3 = declassify(_commitAlice3)
126    })
127    Alice.publish(commitAlice3)
128    commit()
129
130
131    unknowable(Bob, Alice(_handAlice3, _saltAlice3))
132    Bob.only(() => {
133        const handBob3 = declassify(interact.getHand2())
134    })
135    Bob.publish(handBob3)
136    commit()
137
138    Alice.only(() => {
139        const saltAlice3 = declassify(_saltAlice3)
140        const handAlice3 = declassify(_handAlice3)
141    })
142
143    Alice.publish(saltAlice3, handAlice3)
144    checkCommitment(commitAlice3, saltAlice3, handAlice3)
145
146    const outcome3 = winner(handAlice3, handBob3)
```
* From Line 122 to 126 we use the gethand2 function to get the hand alice plays for the third round, we then make a commitment to hide the hand until the second player publishes their hand.
* On line 127 and 128 we publish this commitment and commit.
* On Line 131 we use the unknowable function to ensure that Bob doesn't know Alice hand.
* From line 132 to 134 we use the gethand1 function to get Bob's hand for the second round of the game, then we publish and commit on line 135 and 136.
* From line 138 to 143 we reveal Alice hand and publish it for everyone to see.
* On line 144 we use the checkCommitment function to ensure the commitment published above by alice wasn't tampered with.
* On line 146 we use the winner function to determine winner of the final found.

```js
147    const [forAlice, forBob] =
148        outcome2 == A_WINS && outcome == A_WINS || outcome == A_WINS && outcome3 == A_WINS || outcome2 == A_WINS &&outcome3 == A_WINS ? [2, 0] :
149            outcome2 == B_WINS && outcome == B_WINS || outcome == B_WINS && outcome3 == B_WINS || outcome2 == B_WINS && outcome3 == B_WINS ? [0, 2] :
150                [1, 1] /* tie */
151
152    transfer(forAlice * wager).to(Alice)
153    transfer(forBob * wager).to(Bob)
154    commit()
155
156
157    each([Alice, Bob], () => {
158        interact.seeOutcome(outcome3)
159    })
160 })
```
* From line 147 to 150 we create a logic that determines the winner from the different outcomes of the 3 rounds
* On line 152 and 153 we handle the transfers depending on the outcome of the logic created above, we then commit on line 154.
* The code on line 157 to 159 displays the winner of the final round.
Now lets see how all this is implemented in the frontend code

```py
89   def play_alice():
90          num = input("Enter your wager player1: ")
91          rpc_callbacks(
92              "/backend/Alice",
93              ctc_alice,
94              dict(
95                  wager=rpc("/stdlib/parseCurrency", num), deadline=10, **player(player_1)
96              ),
98          )
99
100   alice = Thread(target=play_alice)
101   alice.start()
```
* From line 89 to line 98 we create a function play_alice(), this function will be used to execute player1( which is alice) functions in the game, this is done on line 100 and 101 using the thread function
```py
102    def play_bob():
103        wag =input("Do you accept wager player2: ")
104        if wag == "yes" or wag == "y" or wag == "Y" or wag == "YES":
105
106            def acceptWager(amt):
107                print("%s accepts the wager of %s" % (player_2, fmt(amt)))
108
109            ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
110            rpc_callbacks(
111                "/backend/Bob",
112                ctc_bob,
113               dict(acceptWager=acceptWager, **player(player_2)),
114            )
115            rpc("/forget/ctc", ctc_bob)
116        elif wag == "n" or wag == "no" or wag == "NO" or wag == "N":
117            print("wager not accepted")
118            quit()
119
120    bob = Thread(target=play_bob)
121    bob.start()
```
* From line 102 to line 118 we also a create a function play_bob(), this is used to execute player2 functionalities in the game. we also use the thread function to execute the function on line 120 and line 121. 
```py
122    alice.join()
123    bob.join()
124
125    after_alice = get_balance(acc_alice)
126    after_bob = get_balance(acc_bob)
127
128    print("%s went from %s to %s" % (player_1,before_alice, after_alice))
129    print("%s went from %s to %s" % (player_2,before_bob, after_bob))
130
131    rpc("/forget/acc", acc_alice, acc_bob)
132    rpc("/forget/ctc", ctc_alice)
133
134
135 if __name__ == "__main__":
136    main()

```
* On line 122 and 123 we use the .join() to instructs the main thread to wait until both child threads have run to completion, signifying the end of the game.
* From line 125 to 129  we create variables to store the balance of the two participants and print them out on line 128 and 129.
* On line 131 and 132 we forget the contracts just incase the players want to play again.
* On line 135 and 136 we run the main() function. 
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
