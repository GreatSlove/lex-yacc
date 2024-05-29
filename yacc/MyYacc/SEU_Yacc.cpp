#include <iostream>
#include "helper.h"
//#include "LR1ToLALR.h"
#include "First.h"
#include "CFGToLRDFA.h"
#include "Parse_Yacc.h"
//#include "Parsing.h"
//#include "CodeGeneration.h"
extern map<int, set<int> > firstMap;

using namespace std;
int main() {

    string filepath = "./yacc.y";
    Parse_Yacc(filepath,GlobalSymbolVec,GlobalProductionVec,GlobalProducerVec,FuncVec);

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