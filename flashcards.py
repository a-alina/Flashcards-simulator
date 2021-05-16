from sys import exit
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcards.db?check_same_thread=False')

Base = declarative_base()

class Flashcard(Base):
    __tablename__ = 'Flashcards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.box = 0

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def menu():

    while True:
        print("""1. Add flashcards
2. Practice flashcards
3. Exit """)

        choice = input()

        if choice == '1':
            add_menu()
        elif choice == '2':
            practice()
        elif choice == '3':
            print('Bye!')
            exit()
        else:
            print(f"{choice} is not an option")

def add_menu():
    while True:
        print("""1. Add a new flashcard
2. Exit""")
        choice = input()

        if choice == '1':
            add_card()
        elif choice == '2':
            menu()
        else:
            print(f'{choice} is not an option')

def add_card():

    while True:
        question = input('Question:\n')
        if question.count('?') == 1:
            break
    while True:
        answer = input('Answer:\n')
        if answer != '':
            break

    new_card = Flashcard(question, answer)
    session.add(new_card)
    session.commit()
    add_menu()

def update(row):
    data_list = session.query(Flashcard).all()
    choice = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n')
    while True:
        if choice == 'd':
            session.delete(row)
            session.commit()
            practice()
        elif choice == 'e':
            question = input(f"current question: {row.question}\nplease write a new question:")
            row.question = question
            answer = input(f"current answer: {row.answer}\nplease write a new answer:")
            row.answer = answer
            session.commit()
            break
        else:
            print(f"{choice} is not an option")

def practice():

    result_list = session.query(Flashcard).all()

    if len(result_list) == 0:
        print('There is no flashcard to practice!')
        menu()
    else:
        for i in range(len(result_list)):
            print(f'Question: {result_list[i].question}')
            while True:
                choice = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n')
                if choice == 'y':
                    print(f'Answer: {result_list[i].answer}')
                    answer(result_list[i])
                    break
                elif choice == 'n':
                    answer(result_list[i])
                    pass
                    break
                elif choice == 'u':
                    update(result_list[i])
                    break
                else:
                    print(f"{choice} is not an option")
        menu()

def answer(row):

    while True:
        choice = input('''press "y" if your answer is correct:\npress "n" if your answer is wrong:\n''')
        if choice == 'y':
            row.box += 1
            break
        elif choice == 'n':
            row.box = 0
            break
        else:
            print(f"{choice} is not an option")

    if row.box == 3:
        session.delete(row)
    session.commit()

menu()
