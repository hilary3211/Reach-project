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

```js
- 'reach 0.1';
- const [isHand, ROCK, PAPER, SCISSORS] = makeEnum(3)
3.
4. const [isOutcome, B_WINS, DRAW, A_WINS] = makeEnum(3) 
5
6 const winner = (handA, handB) => ((handA + (4 - handB)) % 3)
7 
8
9 assert(winner(ROCK, PAPER) == B_WINS)
10 assert(winner(PAPER, ROCK) == A_WINS)
11 assert(winner(ROCK, ROCK) == DRAW)
12
13 forall(UInt, handA =>
14    forall(UInt, handB =>
15       assert(isOutcome(winner(handA, handB)))))
16
17 forall(UInt, (hand) =>
18    assert(winner(hand, hand) == DRAW))
```

* As you know Line 1 is used to specify the version of reach 
* From line 2 to 6 we create functions and variables we use within the program
* From line 9 to 18 ensures that all the the functions work using the assert function

Now lets dive into creating the participant of the game Alice and Bob.  The first step is to create the functions which will be used by both participant frontend to communicate with the reach backend code. 

```js
20 const Player = { 
21    ...hasRandom,
22    getHand: Fun([], UInt), 
23    getHand1: Fun([], UInt), 
24    getHand2: Fun([], UInt),
25    seeOutcome: Fun([UInt], Null),
26    informTimeout: Fun([], Null)
27 };
28
29 export const main = Reach.App(() => {
30    const Alice = Participant('Alice', {
31        ...Player,
32        wager: UInt,
33        deadline: UInt
34    });
35    const Bob = Participant('Bob', {
36        ...Player,
37        acceptWager: Fun([UInt], Null),
38    });
39
40    init();
```
* Line 20 to Line 27 defines the functions the two participants have in common. These functions are all stored in a variable name called Player 
* Line 29 to Line 38 creates the participants of the game and includes their functions

* Line 40 is used to initalize the creation participants

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
13
14    
15
16    def fmt(x):
17        return rpc("/stdlib/formatCurrency", x, 4)
18
19    def get_balance(w):
20        return fmt(rpc("/stdlib/balanceOf", w))
21
22    before_alice = get_balance(acc_alice)
23    before_bob = get_balance(acc_bob)
24
25    print("%s starting balance is %s algo" %(player_1,before_alice))
26    print("%s starting balance is %s algo"%(player_2,before_bob))
27
28    ctc_alice = rpc("/acc/contract", acc_alice)
29
30    OUTCOME = [
31        "%s wins" %(player_2),
32        "Draw",
33        "%s wins"%(player_1),
34    ]
35    HAND = ["Rock", "Paper", "Scissors"]
36    Hands = {
37        "Rock": 0,
38        "R": 0,
39        "r": 0,
40        "Paper": 1,
41        "P": 1,
42        "p": 1,
43        "Scissors": 2,
44        "S": 2,
45        "s": 2,
46    }
```
* From line 2 to line 4 we are simply importing modules we will use in the frontend code, like the rpc server which will be used to connect our frontend python code to the reach backend code.

* On line 6 the Python program binds rpc and rpc_callbacks out of mk_rpc. These two functions are the only tools we will need to communicate with the RPC server.
* From line 8 to line 12 we are simply creating test account, account names of the players and funding those accounts 
* From line 16 to line 20 we create two functions, the fmt function is used to format the account balance to 4 decimal places, while the getbalance function is used to the balance of the test accounts used in the game
* From line 22 to line 26 we are simply trying to get the balance to the account before the game begins and print it out  
* On Line 28 we are deploying the contract 
* From line 30 to line 46 we create a dictionary ad lists used within the program 

So now we are going to create the functions, using the the same function names we used in the reach backend code above 

```py
48 def player(who):
49        def getHand():
50            time.sleep(5)
51            if who == player_1:
52                hand = input("Enter your hand player1: ")
53            elif who == player_2:
54                hand = input("Enter your hand player2: ")
55            selected_hand = Hands[hand]
56            return selected_hand
57        
58        def getHand1():
59            time.sleep(5)
60            if who == player_1:
61                hand = input("Enter your hand player1: ")
62            elif who == player_2:
63                hand = input("Enter your hand player2: ")
64            selected_hand = Hands[hand]
65            return selected_hand
66
67        def getHand2():
68            time.sleep(5)
69            if who == player_1:
70                hand = input("Enter your hand player1: ")
71            elif who == player_2:
72                hand = input("Enter your hand player2: ")
73            selected_hand = Hands[hand]
74            return selected_hand
75        
76        def informTimeout():
77            print("%s observed a timeout" % who)
78
79        def seeOutcome(n):
80            print(
81                "%s saw outcome %s this round"
82                % (who, OUTCOME[rpc("/stdlib/bigNumberToNumber", n)])
83            )
84
85        return {
86            "stdlib.hasRandom": True,
87            "getHand": getHand,
88            "getHand1": getHand1,
89            "getHand2": getHand2,
90            "informTimeout": informTimeout,
91            "seeOutcome": seeOutcome,
92        }
```
* On line 48 we create the general player function with the player name argument. This main player function contains sub functions which has all the functionality the players in the game posses 
* Line 49 to Line 56 contains the first gethand function which is used to get the hands of the users in the first round of the game.
* Line 58 to Line 65 contains the second gethand function which is used to get the hands of the two players in the second round of the game.
* Line 67 to line 74 contains the third gethand function which is used to get the hands of the two players in third round of the game 
* Line 76 to line 77 contains the function built to help inform timeouts in game 
* Line 78 to line 83 contains a function that is used in the program to see the outcome each round 
* On line 85 to line 91 we simply return this subfunctions of the main player function.
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
60    Bob.only(() => {
61        interact.acceptWager(wager)
62    })
63    Bob.pay(wager)
64    commit()
65    Alice.only(() => {
66        const _handAlice = interact.getHand()
67        const [_commitAlice, _saltAlice] = makeCommitment(interact, _handAlice)
68        const commitAlice = declassify(_commitAlice)
69    })
70    Alice.publish(commitAlice)
71    commit()
72
73    unknowable(Bob, Alice(_handAlice, _saltAlice))
74
75    Bob.only(() => {
76        const handBob = declassify(interact.getHand())
77    })
78    Bob.publish(handBob)
79    commit()
80
81    Alice.only(() => {
82        const saltAlice = declassify(_saltAlice)
83        const handAlice = declassify(_handAlice)
84    })
85
86    Alice.publish(saltAlice, handAlice)
87
88    checkCommitment(commitAlice, saltAlice, handAlice)
89    const outcome = winner(handAlice, handBob)
90    each([Alice, Bob], () => {
91        interact.seeOutcome(outcome)
92    })
93    commit()
```
In this index.rsh file above we use some of the fuctions we defined in the index.py frontend code. We use the gethand function to get the hands of both players for the first round and also we use the seeOutcome function to see the outcome of the first round. 
* In line 56 to line 84 we are using to gethand function to get the players hand, then we make a commitment to hide the first players hand till the second player reveals their hands 

The code below does exactly the same as the one above but it uses the gethand1 and gethand2 function to get the players hands for the second round and the last round. Towards the end of the index.rsh we use a computation to determine the winner of the 3 rounds and transfer the funds in the contract to winner , or in the case of a draw the funds will be transfered back to the two players.
```js
95 Alice.only(() => {
96        const _handAlice2 = interact.getHand1()
97        const [_commitAlice2, _saltAlice2] = makeCommitment(interact, _handAlice2)
98        const commitAlice2 = declassify(_commitAlice2)
99    })
100    Alice.publish(commitAlice2)
101    commit()
102
103
104    unknowable(Bob, Alice(_handAlice2, _saltAlice2))
106    Bob.only(() => {
107        const handBob2 = declassify(interact.getHand1())
108    })
109    Bob.publish(handBob2)
110    commit()
111
112    Alice.only(() => {
113        const saltAlice2 = declassify(_saltAlice2)
114        const handAlice2 = declassify(_handAlice2)
115    })
116
117    Alice.publish(saltAlice2, handAlice2)
118    checkCommitment(commitAlice2, saltAlice2, handAlice2)
119
120
121    const outcome2 = winner(handAlice2, handBob2)
122    each([Alice, Bob], () => {
123        interact.seeOutcome(outcome2) 
124    })
125    commit()
126
127     Alice.only(() => {
128        const _handAlice3 = interact.getHand2()
129        const [_commitAlice3, _saltAlice3] = makeCommitment(interact, _handAlice3)
130        const commitAlice3 = declassify(_commitAlice3)
131    })
132    Alice.publish(commitAlice3)
133    commit()
134
135
136    unknowable(Bob, Alice(_handAlice3, _saltAlice3))
137    Bob.only(() => {
138        const handBob3 = declassify(interact.getHand2())
139    })
140    Bob.publish(handBob3)//publishing the hand 
141    commit()
142
143    Alice.only(() => {
144        const saltAlice3 = declassify(_saltAlice3)
145        const handAlice3 = declassify(_handAlice3)
146    })
147
148    Alice.publish(saltAlice3, handAlice3)
149    checkCommitment(commitAlice3, saltAlice3, handAlice3)
150
151
152    const outcome3 = winner(handAlice3, handBob3)
153
154    const [forAlice, forBob] =
155        outcome2 == A_WINS && outcome == A_WINS || outcome == A_WINS && outcome3 == A_WINS || outcome2 == A_WINS && outcome3 == A_WINS ? [2, 0] :
156            outcome2 == B_WINS && outcome == B_WINS || outcome == B_WINS && outcome3 == B_WINS || outcome2 == B_WINS && outcome3 == B_WINS ? [0, 2] :
157                [1, 1] /* tie */
158
159    transfer(forAlice * wager).to(Alice)
160    transfer(forBob * wager).to(Bob)
161    commit();
162
163
164    each([Alice, Bob], () => {
165        interact.seeOutcome(outcome3)
166    })
167 })
```
Now lets see how all this is implemented in the frontend code

```py
93 def play_alice():
94        num = input("Enter your wager player1: ")
95        rpc_callbacks(
96            "/backend/Alice",
97            ctc_alice,
98            dict(
99                wager=rpc("/stdlib/parseCurrency", num), deadline=10, **player(player_1)
100            ),
101        )
102
103    alice = Thread(target=play_alice)
104    alice.start()
105
106    def play_bob():
107        wag =input("Do you accept wager player2: ")
108        if wag == "yes" or wag == "y" or wag == "Y" or wag == "YES":
109
110            def acceptWager(amt):
111                print("%s accepts the wager of %s" % (player_2, fmt(amt)))
112
113            ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
114            rpc_callbacks(
115                "/backend/Bob",
116                ctc_bob,
117                dict(acceptWager=acceptWager, **player(player_2)),
118            )
119            rpc("/forget/ctc", ctc_bob)
120        elif wag == "n" or wag == "no" or wag == "NO" or wag == "N":
121            print("wager not accepted")
122            quit()
123
124    bob = Thread(target=play_bob)
125    bob.start()
126
127    alice.join()
128    bob.join()
129
130    after_alice = get_balance(acc_alice)
131    after_bob = get_balance(acc_bob)
132
133    print("%s went from %s to %s" % (player_1,before_alice, after_alice))
134    print("%s went from %s to %s" % (player_2,before_bob, after_bob))
135
136    rpc("/forget/acc", acc_alice, acc_bob)
137    rpc("/forget/ctc", ctc_alice)
138
139
140 if __name__ == "__main__":
141    main()

```
* From line 93 to line 101 we create a function play_alice(), this function will be used to execute player1( which is alice) functions in the game, this is done on line 103 and 104 using the thread function
* From line 106 to line 122 we also a create a function play_bob(), this is used to execute player2 functionalities in the game. we also use the thread function to execute the function on line 124 and line 125. 
* On line 127 and 128 we use the .join() to instructs the main thread to wait until both child threads have run to completion, signifying the end of the game.
 
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
