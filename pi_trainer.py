import os

pi = 0
with open("pi-decimals.txt", "r") as pi:
    pi = str(pi.read())
    
correct = True
idx = 4

while correct == True:
        
        pi_true = pi[:idx]
        print(pi_true)
        input("press enter to try from memory")
        os.system('cls')

        pi_guess = input("enter pi up to and including the first " + str(idx - 1) + " decimals here:")
        if pi_guess == pi_true:
            print("well done, now try one more decimal!")
            idx += 1
        else:
            print("that is incorrect, your score is: ", idx - 2)
            correct = False

