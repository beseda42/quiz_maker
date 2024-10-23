from pathlib import Path

class user_error(Exception):
    pass

def check_right_quiz(user, quizzes):
    '''Проверка на правильность выбранного теста для прохождения'''
    if user.casefold() in (elem.casefold() for elem in quizzes):
        return True
    print ("Среди предложенных вариантов такого теста нет, попробуйте ещё раз.")
    return False

def check_right_question(line):
    '''Проверка на правильность введенного вопроса в questions.txt'''
    if line.count('~') == 0:
        raise user_error("Ошибка в строке: " + line + "\nЧто-то введено неправильно, проверьте правильность заполнения файла questions.")

def check_right_answer(line):
    '''Проверка на правильность введенного ответа в questions.txt'''
    if line.count('~') > 0:
        raise user_error(
            "Ошибка в строке: " + line + "\nЧто-то введено неправильно, проверьте правильность заполнения файла questions.")

def check_right_answer_existence(answer, question):
    '''Проверка на наличие правильного ответа у вопроса'''
    if len(answer) == 0:
        raise user_error ("Ошибка: в вопросе " + question +" отсутствует правильный ответ.")

def check_correct_input(user, answers):
    '''Проверка на корректность ввода пользователя'''
    if user.casefold() in (elem.casefold() for elem in answers):
        return True
    print("Среди вариантов ответа такого варианта нет, попробуйте ещё раз.")
    return False

def check_right_user_answer(user, right_answers):
    '''Проверка на правильность ответа пользователя'''
    if user.casefold() in (elem.casefold() for elem in right_answers):
        return True
    return False

#Выбор теста
print ("Для прохождения доступны следующие тесты, выберите один из них:")
quizzes = []
for file in (Path(__file__).parent / 'quizzes').iterdir():
    if file.is_file():
        quizzes.append((file.name).partition('.')[0])
        print((file.name).partition('.')[0])

f = False
while not f:
    quiz = input()
    f = check_right_quiz(quiz, quizzes)

questions = [] #Список вопросов
q_n = 0 #Количество вопросов
answers = [] #Список (списков) ответов на вопросы
right_answers = [] #Список правильных ответов
score = [] #Список баллов за вопрос
full_score = 0 #Максимальное количество баллов за тест
user_answers = [] #Список ответов пользователя


#Считывание информации из файла questions.txt
with open("quizzes/"+quiz+".txt", "r", encoding="utf-8") as file:
    c = 0 #Вспомогательная переменная для ввода ответов (c == 0 ввод вопроса, c != 0 ввод ответа)
    t_answers = [] #Вспомогательный массив для ввода ответов
    t_right_answer = [] #Вспомогательный массив для ввода правильных ответов
    for line in file:
        line = line.strip()
        if line != "": #проверка на пустую строку
            if c == 0: #ввод вопроса, количества ответов и баллов за него
                check_right_question(line)
                questions.append(line.partition(' ~ ')[0])
                q_n += 1
                c = int(((line.partition(' ~ ')[2]).partition(' ')[0]).partition('\n')[0])
                if line.count('~') > 1:
                    full_score += int(line.rpartition('~')[2])
                    score.append(int(line.rpartition('~')[2]))
                else:
                    full_score += 1
                    score.append(1)
            else: #ввод ответа
                check_right_answer(line)
                if line[0] == '@':
                    t_right_answer.append(line[1:])
                    t_answers.append(line[1:])
                else: t_answers.append(line)
                c -= 1
                if c == 0:
                    answers.append(t_answers)
                    check_right_answer_existence(t_right_answer, questions[len(questions) - 1])
                    right_answers.append(t_right_answer)
                    t_right_answer = []
                    t_answers = []

i = 0 #примитивный итератор для ходьбы по спискам списков
user_score = 0 #баллы пользователя
q_n_right = 0 #правильные ответы пользователя

for q in questions:
    print("\nВопрос " + str(i+1) + ":\n" + q + "\n\nВарианты ответа:")
    for a in answers[i]:
        print (a)
    print ("\nВаш ответ:")
    f = False
    while not f:
        user = input()
        f = check_correct_input(user, answers[i])
    if check_right_user_answer(user, right_answers[i]):
        q_n_right += 1
        user_score += score[i]
    user_answers.append(user)
    i += 1

print("Правильных ответов на вопрос: " + str(q_n_right) + " из " + str(q_n))
print ("Набрано баллов: " + str(user_score) + " из " + str(full_score))
print ("\nХотите посмотреть отчет о прохождении? (Да/Нет)")

f = False
while not f:
    user = input()
    f = check_correct_input(user, ["Да", "Нет"])

if user.casefold() == "Да".casefold():
    i = 0
    for q in questions:
        print("\nВопрос " + str(i+1) + ":\n" + q + "\n\nВарианты ответа:")
        for a in answers[i]:
            print(a)
        print("\nВаш ответ:\n" + user_answers[i])
        print("\nПравильный ответ:")
        for elem in right_answers[i]:
            print (elem)
        print("\nМаксимальный балл за вопрос: " + str(score[i]))
        i += 1
    print ("\nНа этом всё, но вы можете попробовать пройти другой тест :)")
else: print ("Тогда до скорых встреч!")