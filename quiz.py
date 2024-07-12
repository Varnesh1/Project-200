import socket 
import random

from threading import Thread


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address,port))
server.listen()

list_of_clients = []
questions = [
    " What is the Italian word for pie? \n a.Mozarella\n b.Pasty\n c.Patty\nd .Pizza",
    " Water boils at 212 Units in which scale? \n a.Farenheit\n b.Celsius\n c.Rankine\n d.Kelvin",
    " Which sea creature has three hearts? \n a.Dolphin\n b.Octopus\n c.Walrus\n d.Seal",
    "Who was the character in our childhood rhymes associated with lambs? \n a.Mary \n b.Jack \n c.Johnny \n/Mukhesh",
    ]
answers = ['d','a','b','a']

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index,random_question,random_answer

def remove_question(index)  :
    questions.pop(index)
    answers.pop(index)

def remove(c):
    if c in list_of_clients:
        list_of_clients.remove(c)

def clientthread(conn):
    score = 0
    conn.send('Welcome to the quiz game'.encode('utf-8'))
    conn.send('You will recieve a question. The answer to that question should be a,b,c or d\n'.encode('utf-8'))
    conn.send('Good Luck\n\n'.encode('utf-8'))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            msg = conn.recv(2048).decode('utf-8')
            if msg:
                if msg.lower() == answer:
                    score += 1
                    conn.send("Correct Answer\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer\n\n".encode('utf-8'))
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

while True:
    conn,addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + 'connected')
    thread1 = Thread(target=clientthread,args=(conn))
    thread1.start()