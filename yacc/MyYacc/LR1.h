#ifndef SEUYACC_CFGTOLRDFA_H
#define SEUYACC_CFGTOLRDFA_H

#include"define.h"
extern map<int, set<int> > firstMap;
extern ProducerVec GlobalProducerVec;
extern SymbolVec GlobalSymbolVec;
extern map<int, pair<int, int> > indexMap;
extern int startProduction;

//记录当前LR状态集出边及目标LR状态集
void stateEdge_construct(const vector<Item> &itemList, map<int, ItemSet> &stateMap);
void epsilon_closure(const ItemSet &kernelSet, ItemSet &closureSet);
void first_string(set<int> &firstSet, const vector<int> &symbolSequence);

void CFGToLRDFA(Collection &lrStateCollection) {
    queue<int> stateQueue;
    lrStateCollection.clear();
    Item startItem;
    ItemSet initialItemSet;
    startItem.productionrInt = startProduction; //S'->S
    startItem.prediction.insert(GlobalSymbolVec.size() - 1); //文法结束
    initialItemSet.stateInt = 0; //0号为初始状态
    initialItemSet.itemSet.push_back(startItem);
    lrStateCollection.push_back(initialItemSet);
    stateQueue.push(0);

    while (!stateQueue.empty()) {
        int currentState = stateQueue.front();
        stateQueue.pop();
        ItemSet closureSet;
        epsilon_closure(lrStateCollection[currentState], closureSet);
        map<int, ItemSet> transitionMap;
        stateEdge_construct(closureSet.itemSet, transitionMap);
        for (auto &transition : transitionMap) {
            int numStates = lrStateCollection.size(), targetState = -1;
            for (size_t i = 0; i < numStates; i++)
                if (lrStateCollection[i] == transition.second) {
                    targetState = i;
                    break;
                }
            if (targetState != -1) {
                lrStateCollection[currentState].edgeMap[transition.first] = targetState;
                continue;
            } else {
                transition.second.stateInt = numStates;
                lrStateCollection.push_back(transition.second);
                lrStateCollection[currentState].edgeMap[transition.first] = numStates;
                stateQueue.push(numStates);
            }
        }
    }
}

void epsilon_closure(const ItemSet &kernelSet, ItemSet &closureSet) {
    set<int> inQueue;
    map<pair<int, int>, int> itemIndex;
    queue<int> itemQueue;
    int counter = 0;
    closureSet.stateInt = -1;
    closureSet.itemSet.clear();
    closureSet.edgeMap.clear();
    for (auto &item : kernelSet.itemSet) {
        closureSet.itemSet.push_back(item);
        itemIndex.emplace(make_pair(item.dot_positionInt, item.productionrInt), counter);
        inQueue.insert(counter);
        itemQueue.push(counter);
        counter++;
    }
    pair<int, vector<int>> production;
    int position, symbol;
    while (!itemQueue.empty()) { //队列未空时
        auto &items = closureSet.itemSet;
        production = GlobalProducerVec[items[itemQueue.front()].productionrInt];
        position = items[itemQueue.front()].dot_positionInt;
        set<int> &predictiveSymbols = items[itemQueue.front()].prediction;
        inQueue.erase(itemQueue.front()); //踢出队列
        if (position == production.second.size()) { //点在末尾，不用处理
            itemQueue.pop();
            continue;
        }
        symbol = production.second[position]; //需进行处理的符号
        if (GlobalSymbolVec[symbol].isTerminal) { //终结符不用处理
            itemQueue.pop();
            continue;
        }
        auto indexRange = indexMap[symbol];
        unordered_set<int> inputSymbols;
        //求预测符
        vector<int> followingSymbols;
        for (int i = position + 1; i < production.second.size(); ++i) {
            followingSymbols.push_back(production.second[i]);
        }
        set<int> predictionSymbols;
        first_string(predictionSymbols, followingSymbols);
        if (predictionSymbols.count(-1)) { //有epsilon
            predictionSymbols.erase(-1);
            predictionSymbols.insert(predictiveSymbols.cbegin(), predictiveSymbols.cend());
        }
        itemQueue.pop();
        for (int i = indexRange.first; i < indexRange.first + indexRange.second; i++) {
            if (itemIndex.count(make_pair(0, i))) {
                int idx = itemIndex[make_pair(0, i)], setSize = items[idx].prediction.size();
                items[idx].prediction.insert(predictionSymbols.cbegin(), predictionSymbols.cend());
                if (setSize < items[idx].prediction.size()) {
                    if (inQueue.find(idx) == inQueue.end()) {
                        inQueue.insert(idx);
                        itemQueue.push(idx);
                    }
                }
            } else {
                Item newItem;
                newItem.productionrInt = i;
                newItem.prediction = predictionSymbols;
                int itemIdx = items.size();
                itemIndex.emplace(make_pair(0, i), itemIdx);
                itemQueue.push(itemIdx);
                inQueue.insert(itemIdx);
                items.push_back(newItem);
            }
        }
    }
}

void stateEdge_construct(const vector<Item> &itemList, map<int, ItemSet> &stateMap) {
    pair<int, vector<int>> production;
    Item newItem;
    int transitionSymbol;
    for (const auto &lrItem : itemList) {
        production = GlobalProducerVec[lrItem.productionrInt];
        if (production.second.size() == lrItem.dot_positionInt)
            continue;
        transitionSymbol = production.second[lrItem.dot_positionInt];
        newItem = lrItem;
        newItem.dot_positionInt++;
        auto it = stateMap.find(transitionSymbol);
        if (it == stateMap.end()) {
            ItemSet newState;
            newState.itemSet.push_back(newItem);
            stateMap.emplace(transitionSymbol, newState);
        } else {
            it->second.itemSet.push_back(newItem);
        }
    }
}

#endif