#include <iostream>
#include "define.h"
#include "LR1ToLALR.h"
#include "First.h"
#include "LR1.h"
#include "parse.h"
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

    string filepath = "./c99.y";
    Parse_Yacc(filepath,GlobalSymbolVec,GlobalProductionVec,GlobalProducerVec,FuncVec);


    PrintGlobalProductionVec();
    cout<<"\n..Parse yacc.y..\n";

    Collection LR1;
    calc_first();
    cout<<"\n..calculate First set..done\n";

    CFGToLRDFA(LR1);
    cout<<"\n..Construct LR(1) DFA..done\n";

    //printCollection(LR1);
    Parse_Table p1;
    LR1ToTable(LR1,p1);
    cout << "\n..Construct LR(1) Parsing Table..done\n";
    Print_ParsingTable2(p1,"LRParsingTable.csv");

    Collection LALRCollectionTestcase;
    LR1ToLALR(LR1, LALRCollectionTestcase);
    cout << "\n..Construct LALR DFA..done\n";
    

    Parse_Table p2;
    LR1ToTable(LALRCollectionTestcase, p2);
    cout << "\n..Construct LALR Parsing Table..done\n";

    Print_ParsingTable2(p2,"LALRParsingTable.csv");

	system("pause");
    return 0;
}