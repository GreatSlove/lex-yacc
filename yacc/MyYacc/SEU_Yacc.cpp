#include <iostream>
#include "helper.h"
//#include "LR1ToLALR.h"
#include "First.h"
#include "CFGToLRDFA.h"
#include "Parse_Yacc.h"
//#include "Parsing.h"
//#include "CodeGeneration.h"
extern map<int, set<int> > firstMap;


void PrintGlobalProductionVec() {
    for (size_t i = 0; i < GlobalProductionVec.size(); ++i) {
        // 打印数字
        cout << i + 1 << ": ";
        
        // 获取产生式
        const auto &production = GlobalProductionVec[i];
        const string &left = production.first;
        const vector<string> &right = production.second;
        
        // 打印左部
        cout << left << " -> ";
        
        // 打印右部
        for (size_t j = 0; j < right.size(); ++j) {
            cout << right[j];
            if (j < right.size() - 1) {
                cout << " ";
            }
        }
        cout << endl;
    }
}

using namespace std;
int main() {

    string filepath = "./yacc.y";
    Parse_Yacc(filepath,GlobalSymbolVec,GlobalProductionVec,GlobalProducerVec,FuncVec);


    PrintGlobalProductionVec();
    cout<<"\n------------Parse yacc.y.........done\n";

    Collection LR1;
    calc_first();
    cout<<"\n------------calculate First set.........done\n";

    CFGToLRDFA(LR1);
    cout<<"\n------------Construct LR(1) DFA.........done\n";


    printCollection(LR1);
	system("pause");
    return 0;
}