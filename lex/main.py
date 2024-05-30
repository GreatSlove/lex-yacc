# main.py
# Author: Furina-Focalors
# Date: 2024.05.29
from CodeGenerator import generate_code
from NFA import *
from YyLexReader import *
from RegexNormalizer import *
from DFA import *

DFA_file = None

print('Reading lex file...')

yyl = YyLexReader("./lex/c99.l")

print("Done.")
print('-------------------')
print("Normalizing...")

regexes = []

for regex,_ in yyl.rules:
    result = RegexNormalizer.normalize(regex,yyl.supportDefinitions)
    #print(result)
    regexes.append(result)

print("Done.")
print('-------------------')
print("Adding dots...")

dotted_regexes=[]
for regex in regexes:
    dotted_regexes.append(RegexNormalizer.add_dots(regex))
# for regex in dotted_regexes:
#     print(regex)

print("Done.")
print('-------------------')
print("Transferring infix to postfix...")

postfix_regexes=[]
for regex in dotted_regexes:
    postfix_regexes.append(RegexNormalizer.infix_to_postfix(regex))
# for regex in postfix_regexes:
#     print(regex)

print("Done.")
print('-------------------')

print('Generating NFA...')

nfas = []

for regex, (_, semantic_rule) in zip(postfix_regexes, yyl.rules):
    # print('Corresponding regex: ', regex)
    nfa = reg_to_nfa(regex, semantic_rule)
    # nfa.print()
    nfas.append(nfa)

# for nfa in nfas:
#     print(nfa.acceptActionMap)

final_nfa = merge_nfa(nfas)
# final_nfa.print()
# assert(EPSILON not in final_nfa.alphabet)

for state,semantic_rule in final_nfa.acceptActionMap.items():
    print(state,':',semantic_rule)

print("Done.")
print('-------------------')

print('Generating DFA...')

if DFA_file:
    dfa = DFA()
    dfa.read_from_file(DFA_file)
else:
    dfa = nfa_to_dfa(final_nfa)
    dfa.write_to_file('dfa.bin')
    # dfa.print()


print("Done.")
print('-------------------')
print("Minimizing...")

dfa.minimize()
dfa.write_to_file('minimized.bin')

print("Done.")
print('-------------------')

print("Generating lex.yy.c...")

generate_code(dfa,yyl.userProgramHeaders,yyl.userProgram)

print("Done.")
print('-------------------')