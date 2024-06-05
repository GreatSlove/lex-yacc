#ifndef SEUYACC_HELPER_H
#define SEUYACC_HELPER_H

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <map>
#include <vector>
#include <queue>
#include <iostream>
using namespace std;

typedef struct Item {
    int dot_positionInt = 0;      //点的位置
    int productionrInt = -1;      //表达式文法标号
    set<int> prediction;         //lookahead
    inline bool operator==(const Item& item)const {
        if (dot_positionInt != item.dot_positionInt ||
            productionrInt != item.productionrInt ||
            prediction != item.prediction
                )
            return false;
        else
            return true;
    }

    Item& operator=(const Item&item) {
        dot_positionInt = item.dot_positionInt;
        productionrInt = item.productionrInt;
        prediction.clear();
        prediction.insert(item.prediction.cbegin(), item.prediction.cend());
        return *this;
    }
    Item(){}
    Item(int a, int b, set<int>c) {
        dot_positionInt = a;
        productionrInt = b;
        prediction = c;
    }

}Item;


//LR1项目
typedef struct ItemSet {
    int stateInt = -1;                    //状态号
    unordered_map<int, int> edgeMap;     //<字符标号，状态号>
    vector<Item> itemSet;        //项目集内各项目

    inline bool operator==(const ItemSet& BSet)const {
        int la = itemSet.size(), lb = BSet.itemSet.size();
        if (la != lb)
            return false;
        for (int i = 0; i < la; i++) {
            int j = 0;
            for (; j < lb; j++)
                if (itemSet[i] == BSet.itemSet[j])break;
            if (j == lb)return false;
        }
        return true;
    }
}ItemSet;

//LR1项目集
typedef vector<ItemSet> Collection;

typedef struct Symbol {
    string symbol;        
    bool isTerminal;      
}Symbol;

//存放Symbol的全局变量
typedef vector<Symbol> SymbolVec;
SymbolVec GlobalSymbolVec;

//产生式
typedef vector<pair<string, vector<string> > > ProductionVec;
ProductionVec GlobalProductionVec;

//存放产生式的数字版本
typedef vector<pair<int, vector<int> > > ProducerVec;
ProducerVec GlobalProducerVec;

//分析表
typedef unordered_map<int, unordered_map < int, int > >  Parse_Table;

//对yacc.y文件进行解析,得到产生式vec/辅助函数/Symbol
vector<string> FuncVec;
//存放辅助函数
map<int, pair<int, int> >indexMap;

map<int, set<int> > firstMap;
//存放first集合
int startProduction;


void printSet(const set<int>& s) {
    cout << "{";
    for (auto it = s.begin(); it != s.end(); ++it) {
        if (it != s.begin()) cout << ", ";
        cout << *it;
    }
    cout << "}";
}

// Function to print an Item
void printItem(const Item& item) {
    cout << "Item(dot_positionInt: " << item.dot_positionInt
         << ", productionrInt: " << item.productionrInt
         << ", prediction: ";
    printSet(item.prediction);
    cout << ")";
}

// Function to print an ItemSet
void printItemSet(const ItemSet& itemSet) {
    cout << "ItemSet(stateInt: " << itemSet.stateInt << ", edgeMap: {";
    for (const auto& pair : itemSet.edgeMap) {
        cout << " (" << pair.first << " -> " << pair.second << ")";
    }
    cout << " }, itemSet: [";
    for (const auto& item : itemSet.itemSet) {
        printItem(item);
        cout << ", ";
    }
    cout << "])\n";
}

// Function to print the Collection
void printCollection(const Collection& collection) {
    cout << "Collection contains " << collection.size() << " ItemSets:\n";
    for (const auto& itemSet : collection) {
        printItemSet(itemSet);
    }
}

#endif
