<p align="center">
  <a href="" rel="noopener">
 <img src="https://docs.reach.sh/assets/logo.png" alt="Project logo"></a>
</p>
<h3 align="center">Loopable Rock, Paper, Scissors</h3>

<div align="center">


</div>

---

<p align="center"> Workshop : Loopable Rock,Paper, Scissors
    <br> 
</p>

This workshop will go through the my Reach decentralized umoja hackathon project the loopable rock, paper, scissors. We are go through and explain the reach program from start to finish.

This worshop assumes that you have gone through the Rock,paper,scissors tutorial which also ensures that you have reach properly installed on your system.

## Problem analysis 
Before writing a program you have understand the problem you trying to solve or the application you are trying to build or the logic you are trying to implement. 
The next step of this analysis is to ask and answer certain questions about the project, this will help you understand the project you are trying to build.
Below are the questions i asked my about this project and thier respective answers.

``` 
What is the logic we are trying to implement in the project 

How can we implement this logic 

What are the informations we need to build this project 

```

# Below are the answers 
```
The logic we are trying to implement is loopable rock,paper,scissors.It is variant of rock, paper, scissors in which moves are submitted in batches (to keep transaction costs low) and the first move alternates between two players.
So we are going to have two participant an attacher and a deployer or Player1 and Player2

Once logic is understood we dive into deep research on the project can be built and we started building!.
```
Now we are diving into the program!!!

## Data Definition
For the next step, we are going to define the data type equivalents of the values used in our answers from the previous section. Also, in this step we'll be deciding what functions our participants will have.

* What functions/values does Deployer need to deploy the game, play and observe outcomes?

* What functions/values does attacher need to attach, play and observe outcomes?

* What functions do both participants have in common?

You should look back at your problem analysis to do this step. Whenever a participant starts off knowing something, then it is a field in the interact object. If they learn something, then it will be an argument to a function. If they provide something later, then it will be the result of a function.

It is very advisable to write the answers you get after you problem analysis in your index.rsh file using comments.

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
This is the start of the reach program, we indicate this by using the 'reach 0.1'. The rest of the code contains variables and functions used to in the program, it also has certain computations that ensure our function works 

```
const Player = { 
    ...hasRandom,
    getHand: Fun([], UInt), 
    getHand1: Fun([], UInt), 
    getHand2: Fun([], UInt),
    seeOutcome: Fun([UInt], Null),
    informTimeout: Fun([], Null)
};
```
Then we'll define each individual participant's unique function, but also pass the generic ones to both.
```
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
We go through through the functions and what they do.

Each of the participant have 5 similar functions which is defined in the Player variable and is futher deployed in each of the participants 

* `getHand` This function gets the first user input of the two participants from the frontend. The function doesn't have an argument, but it returns a UInt from the frontend to the backend. This UInt is used to represent the first hand chosen by the two participants.

* `getHand1` This function gets the second user input of the two participants from the frontend. The function doesn't have an argument, but it returns a UInt from the frontend to the backend. This UInt is used to represent the second hand chosen by the two participants. 

* `getHand2` This function gets the third user input of the two participants from the frontend. The function doesn't have an argument, but it returns a UInt from the frontend to backend. This UInt is used to represent the third hand chosen by the two participants.

* `seeOutcome `  This function is used to the see outcome of each round and the overall winner of the game. This function has one argument which is a UInt and is gotten from the frontend but it returns nothing to the backend(this is indicated by the Null ).

## Communication Construction
Now we can design the structure and flow of communication of our application. Try to write this part considering how the deployer setting and paying the wager, attacher accepting and paying the wager, and both of them taking turns to play would go.

**Stop!** Write down the communication pattern for this program as comments.

Here's what we wrote
```
1. Deployer sets wager, deploys contract and pays wager.
2. Attacher sees, accepts and pays wager.
3. The functions will be used to retrive the hands from the frontend.
4.We have to devise a way to hide the first participant's hand and reveal it when the second participant inputs their hand to ensure that the game is fair annd save. 
5. Program pays winner both wagers or refunds both players in the case of a draw.
```

# Here is the implemetation of what we wrote down

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
    Bob.publish(handBob3) 
    commit()


    Alice.only(() => {
        const saltAlice3 = declassify(_saltAlice3)
        const handAlice3 = declassify(_handAlice3)
    })

    Alice.publish(saltAlice3, handAlice3)

    checkCommitment(commitAlice3, saltAlice3, handAlice3)
    const outcome3 = winner(handAlice3, handBob3)
```

So the code above contains the implemetation the comments 1 to 4 we wrote down.

We used certain functions inbuilt functions to complete most of the task such as 

* `makeCommitment()` this is used to make a commitment that the first participant will publish their hands without changing it after the second participant publishes their hand. This was used for each round.

* `unknowable()` this ennsures that the second participant doesn't know the first participant's hand till they publish their's. it is also used in each round.

```
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
The code above checkes the winner of the game and sends the wagers in the contract to the winner, but in the possibility of a draw it sends back the wagers to the two the participants.

Now we are done writing the reach backend code lets have a look at the full code 

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

## Interaction Introduction
Now we have a complete contract backend and now can write the frontend. You can use any frontend library of your choice. In our case, we have chosen to use Python and Tkinter.
So we have two files we used to create the frontend application, the index.py and rps_game.py. We use a postgresql database to pass user input from the rps_game.py to the index.py which runs the logic of the game.

Just incase you decide to use python and tkinter the code will be provided below 

# index.py 

```
# flake8: noqa
import random
from threading import Thread 
from reach_rpc import mk_rpc
import time 
import psycopg2
hostname = "ec2-3-218-171-44.compute-1.amazonaws.com"
database = "d8d58ci3of9cec"
username = "bubgqsyxbdddup"
pwd = "ef9ebaed10600d914d7ecfec9378d487c80ff05bc6615f0db0396b297c57dd8a"
port_id = "5432"
conn = None
cur = None
Name = []
phrase = []
wager = []
hand1 = []
hand2 = []
hand3 = []
try:
    conn = psycopg2.connect(
        host=hostname, dbname=database, user=username, password=pwd, port=port_id
    )

    cur = conn.cursor()
    cur.execute('SELECT * FROM DATASETS')
    for record in cur.fetchall():
        Name.append(record[1])
        phrase.append(record[2])
        wager.append(record[3])
        hand1.append(record[4])
        hand2.append(record[5])
        hand3.append(record[6])
    conn.commit()

    

except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
def main():
    if Name == hand1:
        print("Dataset empty")
    else:
        rpc, rpc_callbacks = mk_rpc()
        rpc("/stdlib/setProviderByName", "MainNet")
        player_1 = Name[0]
        player_2 = Name[1]

        p1acc_mnemonic = phrase[0]
        p2acc_mnemonic = phrase[1]
    
        acc_alice = rpc("/stdlib/newAccountFromMnemonic", p1acc_mnemonic)
        acc_bob  = rpc("/stdlib/newAccountFromMnemonic", p2acc_mnemonic)
        
        def fmt(x):
            return rpc(
                "/stdlib/formatCurrency", x, 4
            ) 

        def get_balance(w):
            return fmt(
                rpc("/stdlib/balanceOf", w)
            ) 
        before_alice = get_balance(
            acc_alice
        )  
        before_bob = get_balance(
            acc_bob
        )  
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


        def player(who):
            def getHand():
                if who == player_1:
                    hand = hand1[0]
                elif who == player_2:
                    hand = hand1[1]
                selected_hand = Hands[hand]
                return selected_hand
            
            def getHand1():
                if who == player_1:
                    hand = hand2[0]
                elif who == player_2:
                    hand = hand2[1]
                selected_hand = Hands[hand]
                return selected_hand

            def getHand2():
                if who == player_1:
                    hand = hand3[0]
                elif who == player_2:
                    hand = hand3[1]
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

        def play_alice():
            wager1 = wager[0]
            try:
                wager2 = int(wager1)
            except:
                wager2 = float(wager1)
            num = wager2
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
            wag = wager[1]
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
        try:
            conn = psycopg2.connect(
                host=hostname, dbname=database, user=username, password=pwd, port=port_id
            )

            cur = conn.cursor()
            delete_db = "DELETE FROM Datasets WHERE id = %s"
            delete_r = ("1",)
            cur.execute(delete_db, delete_r)

            delete_db1 = "DELETE FROM Datasets WHERE id = %s"
            delete_r1 = ("2",)
            cur.execute(delete_db1, delete_r1)
            conn.commit()

        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        
if __name__ == "__main__":
    main()
```

```
# rps_game.py
import threading
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
from reach_rpc import mk_rpc
import time
import psycopg2

Alice_list = []
Bob_list = []
a = 1
b = 2
ro = Tk()
ro.title("Rock Paper Scissors")
ro.configure(background="black")


def end():
    ro.destroy()


label1 = Label(
    ro,
    font=50,
    text="""
    This is a decentralized application that implements decentralization in a rock, paper scissors game.
    Click Play to begin game
    """,
    bg="black",
    fg="white",
)

b1 = Button(ro, text="Play", command=end)
label1.pack(side="bottom")
b1.pack(side="bottom")
Intro_img = ImageTk.PhotoImage(Image.open("Rps1.png"))
img = Label(
    ro,
    image=Intro_img,
    bg="black",
    fg="white",
)
img.pack(side="top")

ro.mainloop()


def main():
    colour = "black"
    colour2 = "white"
    root = Tk()
    root.title("Rock Paper Scissors")
    root.configure(background=colour)

    def Alice_handupdate():
        hand = Alice_hand_word.get()
        name = name1_word.get()
        if hand == "ROCK" or hand == "rock" or hand == "R" or hand == "r":
            Alice_label.configure(image=Alice_rock_img)
            Alice_textbox.insert(END, "\n%s played Rock" % (name))
        elif hand == "PAPER" or hand == "paper" or hand == "p" or hand == "P":
            Alice_label.configure(image=Alice_paper_img)
            Alice_textbox.insert(END, "\n%s played Paper" % (name))
        elif hand == "SCISSORS" or hand == "scissors" or hand == "S" or hand == "s":
            Alice_label.configure(image=Alice_scissors_img)
            Alice_textbox.insert(END, "\n%s played Scissors" % (name))

    def Alice_handupdate2():
        hand = Alice_hand_word2.get()
        name = name1_word.get()
        if hand == "ROCK" or hand == "rock" or hand == "R" or hand == "r":
            Alice_label.configure(image=Alice_rock_img)
            Alice_textbox.insert(END, "\n%s played Rock" % (name))
        elif hand == "PAPER" or hand == "paper" or hand == "p" or hand == "P":
            Alice_label.configure(image=Alice_paper_img)
            Alice_textbox.insert(END, "\n%s played Paper" % (name))
        elif hand == "SCISSORS" or hand == "scissors" or hand == "S" or hand == "s":
            Alice_label.configure(image=Alice_scissors_img)
            Alice_textbox.insert(END, "\n%s played Scissors" % (name))

    def Alice_handupdate3():
        hand = Alice_hand_word3.get()
        name = name1_word.get()
        if hand == "ROCK" or hand == "rock" or hand == "R" or hand == "r":
            Alice_label.configure(image=Alice_rock_img)
            Alice_textbox.insert(END, "\n%s played Rock" % (name))
        elif hand == "PAPER" or hand == "paper" or hand == "p" or hand == "P":
            Alice_label.configure(image=Alice_paper_img)
            Alice_textbox.insert(END, "\n%s played Paper" % (name))
        elif hand == "SCISSORS" or hand == "scissors" or hand == "S" or hand == "s":
            Alice_label.configure(image=Alice_scissors_img)
            Alice_textbox.insert(END, "\n%s played Scissors" % (name))

    def Bob_handupdate():
        hand = Bob_hand_word.get()
        name = name2_word.get()
        if hand == "ROCK" or hand == "rock" or hand == "R" or hand == "r":
            Bob_label.configure(image=Bob_rock_img)
            Bob_textbox.insert(END, "\n%s played Rock" % (name))
        elif hand == "PAPER" or hand == "paper" or hand == "p" or hand == "P":
            Bob_label.configure(image=Bob_paper_img)
            Bob_textbox.insert(END, "\n%s played Paper" % (name))
        elif hand == "SCISSORS" or hand == "scissors" or hand == "S" or hand == "s":
            Bob_label.configure(image=Bob_scissors_img)
            Bob_textbox.insert(END, "\n%s played Scissors" % (name))

    def Bob_handupdate2():
        hand = Bob_hand_word2.get()
        name = name2_word.get()
        if hand == "ROCK" or hand == "rock" or hand == "R" or hand == "r":
            Bob_label.configure(image=Bob_rock_img)
            Bob_textbox.insert(END, "\n%s played Rock" % (name))
        elif hand == "PAPER" or hand == "paper" or hand == "p" or hand == "P":
            Bob_label.configure(image=Bob_paper_img)
            Bob_textbox.insert(END, "\n%s played Paper" % (name))
        elif hand == "SCISSORS" or hand == "scissors" or hand == "S" or hand == "s":
            Bob_label.configure(image=Bob_scissors_img)
            Bob_textbox.insert(END, "\n%s played Scissors" % (name))

    def Bob_handupdate3():
        hand = Bob_hand_word3.get()
        name = name2_word.get()
        if hand == "ROCK" or hand == "rock" or hand == "R" or hand == "r":
            Bob_label.configure(image=Bob_rock_img)
            Bob_textbox.insert(END, "\n%s played Rock" % (name))
        elif hand == "PAPER" or hand == "paper" or hand == "p" or hand == "P":
            Bob_label.configure(image=Bob_paper_img)
            Bob_textbox.insert(END, "\n%s played Paper" % (name))
        elif hand == "SCISSORS" or hand == "scissors" or hand == "S" or hand == "s":
            Bob_label.configure(image=Bob_scissors_img)
            Bob_textbox.insert(END, "\n%s played Scissors" % (name))

    def Astart():
        w = name1_word.get()
        Alice_textbox.insert(END, "Player1 starts game as %s" % (w))

    def Bstart():
        w = name2_word.get()
        Bob_textbox.insert(END, "Player2 starts game as %s" % (w))

    def exit_gui():
        root.destroy()

    def wagerc():
        wag = int(wager_word.get())
        name = name1_word.get()
        Alice_textbox.insert(END, "\n%s proposed a wager of %s" % (name, wag))

    def acceptwagc():
        wag = acceptwager_word.get()
        name = name2_word.get()
        if wag == "yes" or wag == "y" or wag == "Y" or wag == "YES":
            Bob_textbox.insert(END, "\n%s accepted wager" % (name))
        else:
            Bob_textbox.insert(END, "\n%s didnt accept wager" % (name))

    def A_mnemonic():
        mne = Alice_mnemonic_word.get()
        Alice_textbox.insert(
            END,
            "\n%s inputed mnemonic phrase\nImporting mnemonic phrase......"
            % (player_1),
        )

    def B_mnemonic():
        mne = Bob_mnemonic_word.get()
        Bob_textbox.insert(
            END,
            "\n%s inputed mnemonic phrase\nImporting mnemonic phrase......"
            % (player_2),
        )

    def click():
        Alice_list.append(a)
        Alice_list.append(name1_word.get())
        Alice_list.append(Alice_mnemonic_word.get())
        Alice_list.append(wager_word.get())
        Alice_list.append(Alice_hand_word.get())
        Alice_list.append(Alice_hand_word2.get())
        Alice_list.append(Alice_hand_word3.get())

        Bob_list.append(b)
        Bob_list.append(name2_word.get())
        Bob_list.append(Bob_mnemonic_word.get())
        Bob_list.append(acceptwager_word.get())
        Bob_list.append(Bob_hand_word.get())
        Bob_list.append(Bob_hand_word2.get())
        Bob_list.append(Bob_hand_word3.get())

        hostname = "ec2-3-218-171-44.compute-1.amazonaws.com"
        database = "d8d58ci3of9cec"
        username = "bubgqsyxbdddup"
        pwd = "ef9ebaed10600d914d7ecfec9378d487c80ff05bc6615f0db0396b297c57dd8a"
        port_id = "5432"
        conn = None
        cur = None

        try:
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id,
            )

            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS Datasets")
            create_script = """ CREATE TABLE IF NOT EXISTS Datasets (
                                    id  int PRIMARY KEY,
                                    name varchar(20) NOT NULL,
                                    Phrase varchar(500) NOT NULL,
                                    Wager varchar(10),
                                    Hand1 varchar(10),
                                    Hand2 varchar(10),
                                    Hand3 varchar(10))
            """

            cur.execute(create_script)

            insert_sc = "INSERT INTO Datasets (id, name, Phrase,  Wager, Hand1, Hand2, Hand3) VALUES (%s,%s,%s,%s,%s,%s,%s) "
            insert_val = (
                Alice_list[0],
                Alice_list[1],
                Alice_list[2],
                Alice_list[3],
                Alice_list[4],
                Alice_list[5],
                Alice_list[6],
            )
            cur.execute(insert_sc, insert_val)

            insert_sc1 = "INSERT INTO Datasets (id, name, Phrase,  Wager, Hand1, Hand2, Hand3) VALUES (%s,%s,%s,%s,%s,%s,%s) "
            insert_val1 = (
                Bob_list[0],
                Bob_list[1],
                Bob_list[2],
                Bob_list[3],
                Bob_list[4],
                Bob_list[5],
                Bob_list[6],
            )
            cur.execute(insert_sc1, insert_val1)
            conn.commit()

        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
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
        a1 = Alice_list[4]
        a2 = Alice_list[5]
        a3 = Alice_list[6]

        b1 = Bob_list[4]
        b2 = Bob_list[5]
        b3 = Bob_list[6]

        if (
            a1 == "r"
            and b1 == "r"
            or a1 == "s"
            and b1 == "s"
            or a1 == "p"
            and b1 == "p"
        ):
            Alice_textbox.insert(
                END, "\n%s saw outcome this round ends in a Draw" % (name1_word.get())
            )
            Bob_textbox.insert(
                END, "\n%s saw outcome this round ends in a Draw" % (name2_word.get())
            )
        elif (
            a1 == "r"
            and b1 == "s"
            or a1 == "p"
            and b1 == "r"
            or a1 == "s"
            and b1 == "p"
        ):
            Alice_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name1_word.get(), name1_word.get()),
            )
            Bob_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name2_word.get(), name1_word.get()),
            )
        elif (
            a1 == "r"
            and b1 == "p"
            or a1 == "p"
            and b1 == "s"
            or a1 == "s"
            and b1 == "r"
        ):
            Alice_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name1_word.get(), name2_word.get()),
            )
            Bob_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name2_word.get(), name2_word.get()),
            )

        if (
            a2 == "r"
            and b2 == "r"
            or a2 == "s"
            and b2 == "s"
            or a2 == "p"
            and b2 == "p"
        ):
            Alice_textbox.insert(
                END, "\n%s saw outcome this round ends in a Draw" % (name1_word.get())
            )
            Bob_textbox.insert(
                END, "\n%s saw outcome this round ends in a Draw" % (name2_word.get())
            )
        elif (
            a2 == "r"
            and b2 == "s"
            or a2 == "p"
            and b2 == "r"
            or a2 == "s"
            and b2 == "p"
        ):
            Alice_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name1_word.get(), name1_word.get()),
            )
            Bob_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name2_word.get(), name1_word.get()),
            )
        elif (
            a2 == "r"
            and b2 == "p"
            or a2 == "p"
            and b2 == "s"
            or a2 == "s"
            and b2 == "r"
        ):
            Alice_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name1_word.get(), name2_word.get()),
            )
            Bob_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name2_word.get(), name2_word.get()),
            )
        if (
            a3 == "r"
            and b3 == "r"
            or a3 == "s"
            and b3 == "s"
            or a3 == "p"
            and b3 == "p"
        ):
            Alice_textbox.insert(
                END, "\n%s saw outcome this round ends in a Draw" % (name1_word.get())
            )
            Bob_textbox.insert(
                END, "\n%s saw outcome this round ends in a Draw" % (name2_word.get())
            )
        elif (
            a3 == "r"
            and b3 == "s"
            or a3 == "p"
            and b3 == "r"
            or a3 == "s"
            and b3 == "p"
        ):
            Alice_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name1_word.get(), name1_word.get()),
            )
            Bob_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name2_word.get(), name1_word.get()),
            )
        elif (
            a3 == "r"
            and b3 == "p"
            or a3 == "p"
            and b3 == "s"
            or a3 == "s"
            and b3 == "r"
        ):
            Alice_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name1_word.get(), name2_word.get()),
            )
            Bob_textbox.insert(
                END,
                "\n%s saw outcome %s wins this round"
                % (name2_word.get(), name2_word.get()),
            )

    def play():
        name1.delete(0, END)
        name2.delete(0, END)
        Alice_mnemonic.delete(0, END)
        Bob_mnemonic.delete(0, END)
        wagerb.delete(0, END)
        acceptwagerb.delete(0, END)
        Alice_hand.delete(0, END)
        Bob_hand.delete(0, END)
        Alice_hand2.delete(0, END)
        Bob_hand2.delete(0, END)
        Alice_hand3.delete(0, END)
        Bob_hand3.delete(0, END)
        Alice_textbox.delete("1.0", END)
        Bob_textbox.delete("1.0", END)
        Alice_list.clear()
        Bob_list.clear()

    player_1 = Label(root, font=50, text="Player1", bg=colour, fg=colour2)
    player_2 = Label(root, font=50, text="Player2", bg=colour, fg=colour2)
    player_1.grid(row=0, column=1)
    player_2.grid(row=0, column=3)

    w_name1 = Label(root, font=30, text="Enter name", bg=colour, fg=colour2)
    w_name2 = Label(root, font=30, text="Enter name", bg=colour, fg=colour2)
    w_name1.grid(row=1, column=1)
    w_name2.grid(row=1, column=3)

    name1_word = StringVar()
    name1 = Entry(root, textvariable=name1_word, width=20)
    name1.grid(row=2, column=1)

    name2_word = StringVar()
    name2 = Entry(root, textvariable=name2_word, width=20)
    name2.grid(row=2, column=3)

    Alicestart = Button(root, text="start", command=Astart)
    Bobstart = Button(root, text="start", command=Bstart)
    Alicestart.grid(row=3, column=1)
    Bobstart.grid(row=3, column=3)

    Alice_mne = Label(
        root, font=50, text="Enter account mnemonic", bg=colour, fg=colour2
    )
    Bob_mne = Label(root, font=50, text="Enter account mnemonic", bg=colour, fg=colour2)
    Alice_mne.grid(row=4, column=1)
    Bob_mne.grid(row=4, column=3)

    Alice_mnemonic_word = StringVar()
    Alice_mnemonic = Entry(root, textvariable=Alice_mnemonic_word, width=30, show="*")
    Alice_mnemonic.grid(row=5, column=1)

    Alice_mne_b = Button(root, text="Enter", command=A_mnemonic)
    Alice_mne_b.grid(row=6, column=1)

    Bob_mnemonic_word = StringVar()
    Bob_mnemonic = Entry(root, textvariable=Bob_mnemonic_word, width=30, show="*")
    Bob_mnemonic.grid(row=5, column=3)

    Alice_mne_b = Button(root, text="Enter", command=B_mnemonic)
    Alice_mne_b.grid(row=6, column=3)
    ask_wager = Label(root, font=50, text="Please enter wager", bg=colour, fg=colour2)
    ask_accept = Label(root, font=50, text="Do you accept wager", bg=colour, fg=colour2)
    ask_wager.grid(row=7, column=1)
    ask_accept.grid(row=7, column=3)

    wager_word = StringVar()
    wagerb = Entry(root, textvariable=wager_word, width=30)
    wagerb.grid(row=8, column=1)

    wager_button = Button(root, text="Enter", command=wagerc)
    wager_button.grid(row=9, column=1)

    acceptwager_word = StringVar()
    acceptwagerb = Entry(root, textvariable=acceptwager_word, width=30)
    acceptwagerb.grid(row=8, column=3)

    acceptwager_button = Button(root, text="Enter", command=acceptwagc)
    acceptwager_button.grid(row=9, column=3)

    play_hand_alice = Label(root, font=50, text="Play Hand", bg=colour, fg=colour2)
    play_hand_bob = Label(root, font=50, text="Play Hand", bg=colour, fg=colour2)
    play_hand_alice.grid(row=10, column=1)
    play_hand_bob.grid(row=10, column=3)

    Alice_hand_word = StringVar()
    Alice_hand = Entry(root, textvariable=Alice_hand_word, width=30)
    Alice_hand.grid(row=11, column=1)

    Alicebutton = Button(root, text="Enter", command=Alice_handupdate)
    Alicebutton.grid(row=12, column=1)

    Bob_hand_word = StringVar()
    Bob_hand = Entry(root, textvariable=Bob_hand_word, width=30)
    Bob_hand.grid(row=11, column=3)

    Bobbutton = Button(root, text="Enter", command=Bob_handupdate)
    Bobbutton.grid(row=12, column=3)

    play_hand_alice2 = Label(
        root, font=50, text="Play second move", bg=colour, fg=colour2
    )
    play_hand_bob2 = Label(
        root, font=50, text="Play second move", bg=colour, fg=colour2
    )
    play_hand_alice2.grid(row=13, column=1)
    play_hand_bob2.grid(row=13, column=3)

    Alice_hand_word2 = StringVar()
    Alice_hand2 = Entry(root, textvariable=Alice_hand_word2, width=30)
    Alice_hand2.grid(row=14, column=1)

    Alicebutton2 = Button(root, text="Enter", command=Alice_handupdate2)
    Alicebutton2.grid(row=15, column=1)

    Bob_hand_word2 = StringVar()
    Bob_hand2 = Entry(root, textvariable=Bob_hand_word2, width=30)
    Bob_hand2.grid(row=14, column=3)

    Bobbutton2 = Button(root, text="Enter", command=Bob_handupdate2)
    Bobbutton2.grid(row=15, column=3)

    play_hand_alice3 = Label(
        root, font=50, text="Play Third move", bg=colour, fg=colour2
    )
    play_hand_bob3 = Label(root, font=50, text="Play Third move", bg=colour, fg=colour2)
    play_hand_alice3.grid(row=16, column=1)
    play_hand_bob3.grid(row=16, column=3)

    Alice_hand_word3 = StringVar()
    Alice_hand3 = Entry(root, textvariable=Alice_hand_word3, width=30)
    Alice_hand3.grid(row=17, column=1)

    Alicebutton3 = Button(root, text="Enter", command=Alice_handupdate3)
    Alicebutton3.grid(row=18, column=1)

    Bob_hand_word3 = StringVar()
    Bob_hand3 = Entry(root, textvariable=Bob_hand_word3, width=30)
    Bob_hand3.grid(row=17, column=3)

    Bobbutton3 = Button(root, text="Enter", command=Bob_handupdate3)
    Bobbutton3.grid(row=18, column=3)

    Alice_rock_img = ImageTk.PhotoImage(Image.open("rock1.jfif"))
    Alice_paper_img = ImageTk.PhotoImage(Image.open("paper2.jfif"))
    Alice_scissors_img = ImageTk.PhotoImage(Image.open("scissor1.jfif"))
    Bob_rock_img = ImageTk.PhotoImage(Image.open("rock1.jfif"))
    Bob_paper_img = ImageTk.PhotoImage(Image.open("paper2.jfif"))
    Bob_scissors_img = ImageTk.PhotoImage(Image.open("scissor1.jfif"))

    Bob_label = Label(root, image=Bob_paper_img, bg="black")
    Alice_label = Label(root, image=Alice_paper_img, bg="black")

    Alice_label.grid(row=19, column=1)
    Bob_label.grid(row=19, column=3)

    Alice_textbox = Text(root, height=4, width=30)
    Alice_textbox.grid(row=20, column=1)
    Bob_textbox = Text(root, height=4, width=30)
    Bob_textbox.grid(row=20, column=3)

    enter_button = Button(
        root, text="Enter Data", command=threading.Thread(target=click).start()
    )
    enter_button.grid(row=21, column=1)

    quit_button = Button(root, text="Exit game", command=exit_gui)
    quit_button.grid(row=21, column=2)

    play_again = Button(root, text="Play_again", command=play)
    play_again.grid(row=21, column=3)

    root.mainloop()


if __name__ == "__main__":
    main()
```

Here is a link to repository of the project [Link](https://github.com/hilary3211/Reach-project), it contains a detailed explanation on how to run the applictaion.

## Discussion
Congrats for finishing this workshop. You implemented the gold rush game that runs on the blockchain yourself.

If you found this workshop rewarding please let us know on [the Discord Community](https://discord.gg/AZsgcXu).

Thanks!!