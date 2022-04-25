<p align="center">
  <a href="" rel="noopener">
 <img src="https://docs.reach.sh/assets/logo.png" alt="Project logo"></a>
</p>
<h3 align="center">Loopable Rock, Paper, Scissors</h3>

<div align="center">


</div>

---

<p align="center"> This Project is a loopale rock, paper, scissors implementation on the blockchain
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 Problem Statement <a name = "problem_statement"></a>](#-problem-statement-)
- [🏁 Getting Started <a name = "getting_started"></a>](#-getting-started-)
- [⛓️ Dependencies / Limitations <a name = "limitations"></a>](#️-dependencies--limitations-)
- [🏁 Getting Started <a name = "getting_started"></a>](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🚀 Future Scope <a name = "future_scope"></a>](#-future-scope-)
- [🏁 Getting Started <a name = "getting_started"></a>](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🎈 Usage <a name="usage"></a>](#-usage-)
- [⛏️ Built With <a name = "tech_stack"></a>](#️-built-with-)
- [✍️ Authors <a name = "authors"></a>](#️-authors-)
- [🎉 Acknowledgments <a name = "acknowledgments"></a>](#-acknowledgments-)

## 🧐 Problem Statement <a name = "problem_statement"></a>

Loopable Rock, Paper, Scissors (RPS)
A variant of rock, paper, scissors in which moves are submitted in batches (to keep transaction costs low) and the first move alternates between two players.

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>

- Desktop based
- Internet connection
- It is limited to desktops because, tkinter was used to create the Gui. Tkinter is a python Gui framework which is used to create desktop based applications. it's limitation is that this Gui can't be deployed on the web
- Assess the impact of each limitation in relation to the overall findings and conclusions of your project, and if
  appropriate, describe how these limitations could point to the need for further research. 

## 🚀 Future Scope <a name = "future_scope"></a>
During the course of the Hackathon i couldn't implement a couple of things, which i will try to implement after the hackathon
- The ability to connect your wallet address to the app by clicking a button, currently the application requires players/users to input their mnemonic phrase in other to connect their wallet to the application.
- Ability to access the desktop based application on the web, I plan on using remote desktop to acheive this 

## 🏁 Getting Started <a name = "getting_started"></a>

To get this project running on your local environment for development `docker` and `docker compose ` are needed

### Prerequisites
- ``` python 3> ```
- ```certifi==2020.12.5```
- ```chardet==4.0.0```
- ```idna==2.10```
- ``` Pillow==9.1.0 ```
- ``` psycopg2==2.9.3 ```
- ``` reach-rpc-client==0.1.2.202107081228 ```
- ``` requests==2.25.1 ```
- ``` urllib3==1.26.2 ```
- ``` reach==0.1.9 ```


### Installing
The application was written with two languages, thats why the the installation processes will be seperated 
Python language
Once python is installed the other Prerequisites will be easy to install 
- Python [Install](https://www.python.org/downloads/?msclkid=95fb884bc30d11ec9c77c9d90aa64d9f)
- Pillow - ```pip install pillow```
- Psycopg2 - ```pip install psycopg2```

Reach language
A link will be provided below, the link contains proper documentation on how to to install reach and it python rpc-client
[Click reach installation](https://docs.reach.sh/tut/rps/)
[Python-Reach installation] (https://docs.reach.sh/tut/rps/7-rpc/)


## 🎈 Usage <a name="usage"></a>
- Have a working internet connection 
- Download the Executable desktop application from release section of the repo
- Download the images folder from the repository
- When done downloading this files put the exe file into the image folder, run the application and enjoy
- After each user is done inputing their data click on the 'Enter data' to send your input data to the database which is passed to the rpc-client server to execute the program
- Wait for atleast 10 - 20 seconds, if users want to play again click the 'play again button' else click the exit button



## ⛏️ Built With <a name = "tech_stack"></a>

- [PostgreSQL](https://www.postgresql.org) - Database
- [Heroku](https://www.heroku.com) - Server Framework
- [Tkinter](https://pythonbasics.org/tkinter) - Gui Framework
- [Gougle cloud](https://console.cloud.google.com/) - Server Environment for virtual machine

## ✍️ Authors <a name = "Hilary"></a>

- [@hilary321](https://github.com/hilary3211) - Idea & Initial work


## 🎉 Acknowledgments <a name = "acknowledgments"></a>

- Hat tip to anyone whose code was used
- Thanks to The Reach platform for organizing the bounty hack
