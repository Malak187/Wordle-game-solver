# Code is written by python language that use type inference (the complier deduce datatype based on its usage in the code)
# Implicit declaration ( datatypes are not determined )
# Python supports dynamic binding
# Binding occurs at run time


import random
from turtle import *

#Class binding
class WordleSolver:  
    # All the following functions(methods) are form of function binding and inside each function there are lots of variable bindings
    def __init__(self, filename, population_size, generations):
        #scope of these attributes are objects generated from that class
        self.filename = filename
        self.geneset = self.filename   ## aliasing
        self.population_size = population_size
        self.generations = generations
        self.target = self.generateWords()
        self.guesses = []
        self.my_set = set()

    def loadWords(self):  #Camel notation
        with open(self.geneset, 'r') as file:
            words = file.read().splitlines()
        return words

    def generateWords(self):
        words = self.loadWords() 
        word = random.choice(words)
        return word

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            guess = self.generateWords()
            population.append(guess)
        return population

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, individual):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        index = random.randrange(0, len(individual))
        letter1, letter2 = random.sample(letters, 2)

        if individual[index] == letter1:
            individual = individual[:index] + letter2 + individual[index + 1:]
        else:
            individual = individual[:index] + letter1 + individual[index + 1:]

        return individual

    def get_feedback(self, guess):
        feedback_list = [-1] * 5
        visited = [0] * 26

        for i in range(len(guess)):
            index = ord(guess[i]) - ord('A')

            if guess[i] == self.target[i]:
                feedback_list[i] = 2
                visited[index] += 1
            else:
                feedback_list[i] = 0
        
        for i in range(len(guess)):
            letter_count = self.target.count(guess[i])
            index = ord(guess[i]) - ord('A')

            if guess[i] in self.target and guess[i] != self.target[i]:
                if letter_count > visited[index]:
                    feedback_list[i] = 1
                    visited[index] += 1

        return feedback_list

    def calculate_fitness(self, parent):
        parent_list = self.get_feedback(parent)
        fitness = sum(parent_list)
        return fitness

    def main(self):
        population = self.initialize_population()
        first_guess = self.generateWords()
        print(first_guess)
        
        
        index = random.randrange(0, self.population_size)
        population[index] = first_guess
        self.guesses.append(first_guess)
        self.my_set.add(first_guess)

        for _ in range(self.generations):
            fitness_scores = []
            for individual in population:
                fitness_scores.append(self.calculate_fitness(individual))

            max_fitness = sorted(fitness_scores, reverse=True)[0]
            second_max_fitness = sorted(fitness_scores, reverse=True)[1]

            max_fitness_index = fitness_scores.index(max_fitness)
            second_max_fitness_index = fitness_scores.index(second_max_fitness)

            parent1 = population[max_fitness_index]
            parent2 = population[second_max_fitness_index]

            #Parameter binding

            child1, child2 = self.crossover(parent1, parent2)
            
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)  

            min_fitness = sorted(fitness_scores)[0]
            second_min_fitness = sorted(fitness_scores)[1]

            min_fitness_index = fitness_scores.index(min_fitness)
            second_min_fitness_index = fitness_scores.index(second_min_fitness)

            population[min_fitness_index] = child1
            population[second_min_fitness_index] = child2

            max_fitness_index = fitness_scores.index(sorted(fitness_scores, reverse=True)[0])
            best_individual = population[max_fitness_index]

            if best_individual not in self.my_set and best_individual in self.loadWords():
                print(best_individual)
                self.my_set.add(best_individual)
                self.guesses.append(best_individual)


solver = WordleSolver('WORDS.txt', 500, 1000)
solver.main()

s = Screen()
t = Turtle()
s.screensize(500,500)
t.speed(100)
tracer(0)

x = -350
y = 290

for i in range(3):
    t.width(3)
    t.up()
    t.goto(x,y)
    t.down()
    t.fd(20)
    y -= 10

t.up()
t.goto(10,250)
t.down()
t.write("Wordle", align = "center", font = ("Algerian", 30, "bold"))
t.up()
t.goto(-800,230)
t.down()
t.fd(2000)
t.up()
t.goto(-150,200)
t.down()
t.width(1)
x =- 140
y = 200
t.pencolor("grey")
for _ in range(6):
    t.up()
    t.goto(x,y)
    t.down()
    for _ in range(5):
        for _ in range(4):
            t.fd(50)
            t.rt(90)

        x += 60
        t.up()
        t.goto(x,y)
        t.down()

    x = -140
    y -= 60

t.pencolor("Black")

update()
tracer(1)

f=0
x = -113
y = 155
z = -140
w = 200

#Aliasing
r=x   
q=y

guesses = solver.guesses 
for i in range(len(guesses)):

    t.up()
    t.goto(x,y)
    t.down()
    
    for j in range(5):
        t.speed(2)
        t.write(guesses[i][j], align = "center", font = ("Ariel", 25, "bold"))
        x += 60
        t.up()
        t.goto(x,y)
        t.down()

    feedback_guess = solver.get_feedback(guesses[i])
    
    for j in range(5):
        t.speed(100)
        t.up()
        t.goto(z,w)
        t.down()
        t.speed(5)

        if feedback_guess[j] == 1:
            t.begin_fill()
            t.pencolor("#c8b653")

            for _ in range(4):
                t.fd(50)
                t.rt(90)

            t.color("#c8b653", "#c8b653")
            t.end_fill()

        elif feedback_guess[j] == 2:
            t.begin_fill()
            t.pencolor("#6ca965")

            for _ in range(4):
                t.fd(50)
                t.rt(90)

            t.color("#6ca965", "#6ca965")
            t.end_fill()

        else:
            t.begin_fill()
            t.pencolor("#787c7f")

            for _ in range(4):
                t.fd(50)
                t.rt(90)

            t.color("#787c7f", "#787c7f")
            t.end_fill()        

        t.up()
        t.goto(r,q)
        t.down()
        t.speed(100)
        t.pencolor("White")
        t.write(guesses[i][j], align = "center", font = ("Ariel", 25, "bold"))
        x += 60
        z += 60
        r += 60
        t.speed(10)
        t.pencolor("Black")

    if guesses[i] == solver.target:
        f = 1
        break

    y -= 60
    x = -113
    z = -140
    w -= 60
    r = -113
    q -= 60


if(f):
    t.up()
    t.goto(-70,-200)
    t.down()
    t.begin_fill()
    for i in range(2):
        t.fd(150)
        t.rt(90)
        t.fd(40)
        t.rt(90)
    t.color("Black","Black")
    t.end_fill()
    t.pencolor("White")
    x=-20
    y=-235
    winWords = ["Impressive!", "Magnificent!", "Great!"]
    chosen = random.choice(winWords)

    if chosen == "Impressive!":
        x = -50
    elif chosen == "Magnificent!":
        x = -55

    t.up()
    t.goto(x,y)
    t.down()
    for i in range(len(chosen)):
        t.write(chosen[i], align = "center", font = ("Ariel", 18, "normal"))
        t.up()
        t.fd(12)
        t.down()

else:
    t.up()
    t.goto(-140,-200)
    t.down()
    t.begin_fill()
    for i in range(2):
        t.fd(280)
        t.rt(90)
        t.fd(40)
        t.rt(90)
    t.color("Black","Black")
    t.end_fill()
    t.pencolor("White")
    x=-125
    y=-235
    lose = "Better Luck Next Time!"
    t.up()
    t.goto(x,y)
    t.down()
    for i in range(len(lose)):
        t.write(lose[i], align = "center", font = ("Ariel", 18, "normal"))
        t.up()
        t.fd(12)
        t.down()


t.hideturtle()
t.speed(100)
done()