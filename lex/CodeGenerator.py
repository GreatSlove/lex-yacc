# CodeGenerator.py
# Author: Furina-Focalors
# Date: 2024.05.29
from collections import defaultdict
from DFA import DFA

def modify_dfa(dfa:DFA)->DFA:
    """
    将DFA的状态修改为从1开始递增
    :param dfa:
    :return:
    """
    new_states = set()
    new_moves = defaultdict(list)
    new_start_state = -1
    new_accepting_states = set()
    new_accept_action_map = {}

    next_state = 0
    old_new = {}
    # 构造原状态到新状态的映射，修改状态集
    for state in dfa.states:
        old_new[state] = next_state
        new_states.add(next_state)
        next_state += 1
    # 修改moves
    for from_state, moves in dfa.moves.items():
        for to_state, character in moves:
            new_moves[old_new[from_state]].append((old_new[to_state],character))
    # 修改初态
    new_start_state = old_new[dfa.startState]
    # 修改终态
    for state in dfa.acceptingStates:
        new_accepting_states.add(old_new[state])
    # 修改语义动作
    for state, action in dfa.acceptActionMap.items():
        new_accept_action_map[old_new[state]] = action
    new_dfa = DFA(new_states,new_moves,new_start_state,new_accepting_states,dfa.alphabet)
    new_dfa.acceptActionMap = new_accept_action_map
    return new_dfa


def generate_transform_matrix(dfa:DFA)->str:
    """
    生成转移矩阵
    :param dfa:
    :return:
    """
    code = '''
#define STATE_NUM {}

// Transform matrix. yy_trans_mat[i][j] is the next state transferred to after state i reads the character with ascii=j.
// -1 means no move.
const int yy_trans_mat[STATE_NUM][128] = 
    '''.format(len(dfa.states))
    code += '{\n\t'

    trans_mat = [[-1 for _ in range(128)] for _ in range(len(dfa.states))]
    for from_state,moves in dfa.moves.items():
        for to_state,character in moves:
            trans_mat[from_state][ord(character)] = to_state
    for i in range(len(dfa.states)):
        count = 0  # 用于美化代码
        code += '// ================== STATE {} ==================\n\t'.format(i)
        for j in range(128):
            code += ' '*(4-len(str(trans_mat[i][j]))) + str(trans_mat[i][j]) + ','
            count += 1
            if count == 16:
                code += '\n\t'
                count = 0
        code += '// ================== STATE {} ==================\n\t'.format(i)
    code += '};\n\n'
    return code

def generate_accepting_states(dfa:DFA)->str:
    code = """
// Marks for accepting states. yy_is_accepting[i] == 1 means state i is an accepting state. 
int yy_is_accepting[STATE_NUM] = {\n\t"""
    is_accepting = [0] * len(dfa.states)
    for state in dfa.acceptingStates:
        is_accepting[state] = 1
    count = 0
    for val in is_accepting:
        code += ' '*(4-len(str(val))) + str(val) + ','
        count += 1
        if count == 16:
            code += '\n\t'
            count = 0
    code += '\n};\n\n'
    return code

def generate_switch(dfa:DFA)->str:
    code = """
    switch(cur_accepting_state){
    """
    for state,action in dfa.acceptActionMap.items():
        code += '\tcase {}:\n\t\t'.format(state) + action + '\n\t\tbreak;\n\t'
    code += '\tdefault:\n\t\treturn -1;\n\t}\n}\n\n'
    return code

def generate_yylex(dfa:DFA)->str:
    code = """
// The main program of lex analyzer. Returns the longest token matched on input stream.
int yylex(){
    // Set the default streams to stdin and stdout
    if(!yyin) yyin = stdin;
    if(!yyout) yyout = stdout;

    // read chars from yyin until there is no moves available.
    while(1){
        yy_cur_char = fgetc(yyin);
        if(yy_cur_char==EOF)break;

		++yy_rb_chars;
		++yy_cur_ptr;
		yy_cur_buf[yy_cur_buf_ptr++] = yy_cur_char;

		if(yy_cur_char=='\\n'){
            ++yylineno;
            ++yy_rb_lines;
        }

        // Transfer to another state.
        yy_cur_state = yy_trans_mat[yy_cur_state][yy_cur_char];
		if(yy_cur_state==-1)break;
        // Record the last accepting state to implement the longest match.
        if(yy_is_accepting[yy_cur_state]){
            yy_last_acc_ptr = yy_cur_ptr;
            yy_last_accepting_state = yy_cur_state;
            yy_rb_lines = 0;
			yy_rb_chars = 0;
        }
    }

    // Rollback moves after the last accepting state. The yylex() should start at the first char 
    // after yy_last_accepting_state.
    if(yy_last_accepting_state == -1) return -1;
    fseek(yyin, yy_last_acc_ptr-yy_cur_ptr, SEEK_CUR);
    yylineno -= yy_rb_lines;
    yy_cur_state = START_STATE;
    yy_cur_ptr = yy_last_acc_ptr;
	// copy cur_buf to yytext
	memset(yytext, 0, yy_buf_size);
	yyleng = strlen(yy_cur_buf);
    strcpy(yytext, yy_cur_buf);
    memset(yy_cur_buf, 0, yy_buf_size);
    yy_cur_buf_ptr = 0;
    // Get the current accepting state and do the switch() work. Then reset yy_last_accepting_state and yy_last_acc_ptr.
    int cur_accepting_state = yy_last_accepting_state;
    yy_last_accepting_state = -1;
    yy_last_acc_ptr = -1;

    // Do the switch() work to find the corresponding accept_action."""
    code += generate_switch(dfa)
    return code


def generate_yyless_yymore():
    return """
// Put yytext into input buffer except for the first n chars.
void yyless(int n) {
    int delta = strlen(yytext) - n;
    fseek(yyin, -delta, SEEK_CUR);
    FILE *yyinCopy = yyin;
    // undo yylineno++
    while (delta--) fgetc(yyinCopy) == '\\n' && yylineno--;
}

// Concat the result of yylex() in the next turn to current yytext.
void yymore() {
    char old[1024];
    strcpy(old, yytext);
    yylex();
    strcpy(yytext, strcat(old, yytext));
}

"""

def generate_code(dfa:DFA, header:str, footer:str):
    """
    代码生成的主函数
    :param dfa:
    :param header:
    :param footer:
    :return:
    """
    # 处理dfa的状态编号
    dfa = modify_dfa(dfa)
    code = '''// --------------------------------------------------------
// | Generated by SEULex.                                 |
// | Lex by Furina-Focalors                               |
// | Project repo: https://github.com/GreatSlove/lex-yacc |
// --------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>

FILE* yyin = NULL, *yyout = NULL;

#define START_STATE {}

'''.format(dfa.startState)

    code += '''const int yy_buf_size = 2048;
char yytext[2048] = {0};
char yy_cur_buf[2048] = {0};
int yylineno = 1, yyleng = 0;
int yy_cur_char = 0, yy_cur_ptr = 0, yy_cur_buf_ptr = 0, yy_cur_state = START_STATE;
int yy_last_accepting_state = -1, yy_last_acc_ptr = -1, yy_rb_lines = 0, yy_rb_chars = 0;
# define ECHO 0

'''
    code += header
    code += generate_transform_matrix(dfa)
    code += generate_accepting_states(dfa)
    code += generate_yylex(dfa)
    code += generate_yyless_yymore()
    code += footer
    # 写入lex.yy.c
    with open('lex.yy.c', 'w') as file:
        file.write(code)
