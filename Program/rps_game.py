import threading
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
from reach_rpc import mk_rpc
import time
import psycopg2

# import win32com.client

# VirtualUI = win32com.client.Dispatch("Thinfinity.VirtualUI")
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
# VirtualUI.Start(60)
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

    # VirtualUI.Start(60)
    root.mainloop()


if __name__ == "__main__":
    main()
