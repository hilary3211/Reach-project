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
