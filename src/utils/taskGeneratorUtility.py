from random import randint, choice, sample, shuffle
from icecream import ic 
import os
from collections import Counter

def gen(length, repeats):
    while True:
        a = [True]*(length//2) + [False]*(length//2)
        shuffle(a)
        if not any(all(a[i]==a[i+j] for j in range(repeats+1)) for i in range(length-repeats)):
            return a

def equationGenerator(equationScore: bool, termCount: int = 2):
    # ic(equationScore)
    while True:
        firstTerm = [choice([randint(1, 9), randint(10, 50)])]
        term = firstTerm + sample(range(1, 9), termCount - 1)
        # ic(term)
        if equationScore:
            term.append(sum(term))
        else:
            wrongChoiceForTwo = choice([True, False])
            wrongChoice = choice([
                "plusMinusDelta", 
                "plusMinusDelta2", 
                "minusRandom", 
                # "oldStyle"
                # "minusNotPlus",
            ])
            # ic(wrongChoice)
            if termCount == 2 and wrongChoiceForTwo:
                # ic("minusNotPlus")
                term.append(term[0] - term[1])
            else:
                match wrongChoice:
                    case "plusMinusDelta":
                        term.append(sum(term) + choice([-1, 1]) * randint(1, 3))
                    case "plusMinusDelta2":
                        term.append(sum(term) + choice([-1, 1]) * 10)
                    case "minusRandom":
                        term.append(sum(term) - choice(term))
                    # case "oldStyle":
                    #     c = randint(0, 50 + termCount*9)
                    #     while c == sum(term):
                    #         c = randint(0, 50 + termCount*9)
                    #     term.append(c)
        if len(term) == termCount + 1 and term[-1] > 0:
            break

    equationText = f"{term[0]}"
    for i in term[1:-1]:
        equationText += f"+{i}"
    equationText += f"={term[-1]}"

    return equationText

EQU_COUNT = 40
BLOCK_COUNT = 10
TERM_COUNT = 4

if not (os.path.exists("taskBlocks")):
    os.makedirs("taskBlocks")

for j in [[2, 3], [4, 10]]:
    for i in range(j[1]):
        genChoices = gen(EQU_COUNT, 2)
        ic(genChoices, Counter(genChoices))
        f = open(os.path.join("taskBlocks", f"block_{j[0]}_{i+1}.txt"), "w")
        for k in range(EQU_COUNT):
            equationScore = genChoices[k]
            # equationScore = choice([True, False])
            # equationScore = False
            f.write(f"{equationGenerator(equationScore, j[0])}\t{int(equationScore)}\n")