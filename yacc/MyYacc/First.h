#ifndef SEUYACC_FIRST_H
#define SEUYACC_FIRST_H

#include "define.h"
extern map<int, set<int> > firstMap;
extern ProducerVec GlobalProducerVec;
extern SymbolVec GlobalSymbolVec;
extern map<int, pair<int, int> > indexMap;

void intersection(set<int>& resultSet, const set<int>& addSet);
void first_symbol(set<int>& resultSet, int& symbol, set<int>& visitedSymbols);
void first_string(set<int>& resultSet, const vector<int>& symbolSequence); 


void first_symbol(set<int>& resultSet, int& currentSymbol, set<int>& visitedSymbols) {

    if (firstMap.count(currentSymbol) != 0) {
        intersection(resultSet, firstMap[currentSymbol]);
        return;
    }
    if (currentSymbol == -1) return;
    if (GlobalSymbolVec[currentSymbol].isTerminal) {
        resultSet.insert(currentSymbol);
        return;
    } else {
        visitedSymbols.insert(currentSymbol);
        auto symbolRange = indexMap[currentSymbol];
        for (int i = symbolRange.first; i < symbolRange.first + symbolRange.second; i++) {
            auto &production = GlobalProducerVec[i];
            int productionSize = production.second.size();
            if (productionSize == 1 && production.second[0] == -1) {
                resultSet.insert(-1);
                continue;
            }
            set<int> tempSet;
            for (int j = 0; j < productionSize; j++) {
                tempSet.clear();
                if (visitedSymbols.find(production.second[j]) != visitedSymbols.end()) {
                    break;
                }
                first_symbol(tempSet, production.second[j], visitedSymbols);
                if (tempSet.count(-1) == 0) {
                    intersection(resultSet, tempSet);
                    break;
                }
                if (j == productionSize - 1) {
                    resultSet.insert(-1);
                    break;
                }
                tempSet.erase(-1);
                intersection(resultSet, tempSet);
            }
        }
    }
}

void intersection(set<int>& resultSet, const set<int>& addSet) {
    resultSet.insert(addSet.cbegin(), addSet.cend());
}

void calc_first() {
    set<int> resultSet, visitedSymbols;
    int symbolCount = GlobalSymbolVec.size();
    for (int currentSymbol = 0; currentSymbol < symbolCount; currentSymbol++) {
        resultSet.clear();
        visitedSymbols.clear();
        first_symbol(resultSet, currentSymbol, visitedSymbols);
        firstMap.emplace(currentSymbol, resultSet);
    }
}

void first_string(set<int>& resultSet, const vector<int>& symbolSequence) {
    if (symbolSequence.size() == 0) {
        resultSet.insert(-1);
        return;
    }
    int sequenceLength = symbolSequence.size();
    for (int i = 0; i < sequenceLength; i++) {
        auto & firstSet = firstMap[symbolSequence[i]];
        if (firstSet.count(-1) == 0) {
            intersection(resultSet, firstSet);
            break;
        }
        if (i == sequenceLength - 1) {
            resultSet.insert(-1);
            break;
        }
        firstSet.erase(-1);
        intersection(resultSet, firstSet);
    }
}

#endif
