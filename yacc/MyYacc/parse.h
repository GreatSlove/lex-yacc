
#ifndef SEUYACC_PARSE_YACC_H
#define SEUYACC_PARSE_YACC_H
#include "define.h"
#include "fstream"
#include "iostream"
#include"map"
#include <stdio.h>

using namespace std;
extern vector<string> FuncVec;
extern vector<Symbol> GlobalSymbolVec;
extern ProductionVec GlobalProductionVec;
extern ProducerVec GlobalProducerVec; 
extern map<int,pair<int,int> >indexMap;
extern int startProduction;
int Parse_Yacc(const string& filename,vector<Symbol>& symbolvec,
               ProductionVec& production,
               ProducerVec& production_int,
               vector<string>&FuncVec){
    ifstream in;
    in.open(filename,ios::in);
    if(!in){
        cout<<"ERROR:Can't open yacc.y!"<<endl;
        return 0;
    }
    //yacc解析
    string str;

    in>>str;
    while(str!="%start"){
        //新行,跳过%token
        if("%token"==str){
            in>>str;
        }
        Symbol item;
        item.symbol=str;
        item.isTerminal=true;
        symbolvec.push_back(item);
        in>>str;
    }


    //2.读入产生式,并存入production
    while(str!="%%")
        in>>str;
    in>>str;

    vector<int> vec_left_int;       //记录在左式出现的int

    //vector<pair<string,vector<string> > > ProductionVec;
    //下次%%是辅助子例程
    int COUNT=0;
    int symbol_index=0;

    while(str!="%%"){
        //开始记录左
        if(str==";")
            in>>str;
        if(str=="%%")
            break;
        string lefr=str;
        int left_int;
        //left 是否在SymbolVec中,并记录其symbol_index
        bool isExist=false;
        bool isQuotation=false;
        bool isT=false;
        if(str[0]=='\''){
            isQuotation=true;
            str=str[1];
            isT=true;
        }


        for(int i=0;i<symbolvec.size();i++){
            if(str==symbolvec[i].symbol){
                symbol_index=i;
                left_int=i;
                isExist=true;
                break;
            }
        }
        if(!isExist){
            symbol_index=symbolvec.size();
            Symbol item;
            item.symbol=str;
            item.isTerminal=false;
            if(isT)
                item.isTerminal=true;
            symbolvec.push_back(item);
            left_int=symbolvec.size()-1;
        }

        vec_left_int.push_back(left_int);

        int left_index=COUNT;
        int right_index=0;
        in>>str;
        if(str==":"){
            in>>str;
        }
        while(str!=";"){
            vector<string> right;
            vector<int> right_int; 
            int count=0;
            do{
                if(str=="\'")
                    count++;
                if(count)
                    count--;

                bool isExist=false;
                bool isQuotation=false;
                bool isT=false;
                if(str[0]=='\''){
                    isQuotation=true;
                    str=str[1];
                    isT=true;
                }
                right.push_back(str);


                for(int i=0;i<symbolvec.size();i++){
                    string temp_symbol="\'"+symbolvec[i].symbol+"\'";
                    if(str==symbolvec[i].symbol||
                       str==temp_symbol){
                        right_int.push_back(i);
                        isExist=true;
                        break;
                    }
                }
                if(!isExist){
                    Symbol item;
                    item.symbol=str;
                    item.isTerminal=false;
                    if(isT)
                        item.isTerminal=true;
                    symbolvec.push_back(item);
                    right_int.push_back(symbolvec.size()-1);
                }

                in>>str;

            }while(str!="|"&&str!=";"&&str!="%%"&&count==0);
            pair<string,vector<string> > production_item(lefr,right);
            production.push_back(production_item);
            pair<int,vector<int> > production_item_int(left_int,right_int);
            production_int.push_back(production_item_int);
            COUNT++;
            right_index++;

            if(str==";")
                continue;
            in>>str;
        }
        pair<int,int> temp(left_index,right_index);
        indexMap[symbol_index]=temp;
    }

    //S'
    int l1=symbolvec.size();
    Symbol item;
    item.symbol="S'";
    item.isTerminal=false;
    symbolvec.push_back(item);

    int prodcution_size=production.size();
    string l="S'";
    vector<string> r{"translation_unit"};
    pair<string,vector<string> > production_item(l,r);
    production.push_back(production_item);
    startProduction = production.size() - 1;
    int trans_item=0;
    for(int i=0;i<symbolvec.size();i++){
        if(symbolvec[i].symbol=="translation_unit")
        {
            trans_item=i;
            break;
        }
    }
    vector<int> vec_l1{trans_item};
    pair<int,vector<int> > production_item_int(l1,vec_l1);
    production_int.push_back(production_item_int);
    pair<int,int> temp(prodcution_size,1);
    indexMap[l1]=temp;

    //$r
    l1 = symbolvec.size();
    Symbol item1;
    item1.symbol = "$r";
    item1.isTerminal = true;
    symbolvec.push_back(item1);

    if(str=="%%")
    {
        while (!in.eof())
        {
            getline(in, str);
            while (str.empty()&&!in.eof())
            {
                getline(in, str);

            }
        }
        FuncVec.push_back(str);
    }
    return 1;
}


#endif
