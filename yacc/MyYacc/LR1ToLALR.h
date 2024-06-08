
#ifndef SEUYACC_LR1TOLALR_H
#define SEUYACC_LR1TOLALR_H

#include <fstream>
#include <iostream>
#include <map>
#include <utility>

#include "define.h"


void Print(const Item item) {
  cout << GlobalProductionVec[item.productionrInt].first << " -> ";
  int dotpos = item.dot_positionInt;
  int i = 0;
  for (i = 0; i < dotpos; i++) {
    cout << GlobalProductionVec[item.productionrInt].second[i] << " ";
  }
  cout << "dot ";
  for (i = dotpos; i < GlobalProductionVec[item.productionrInt].second.size();
       i++) {
    cout << GlobalProductionVec[item.productionrInt].second[i] << " ";
  }

  cout << "---- {";
  for (auto& u : item.prediction) {
    cout << GlobalSymbolVec[u].symbol << " ";
  }
  cout << "}";

  cout << endl;
}

void PrintItemSet(const ItemSet itemset) {
  cout << "I " << itemset.stateInt << " : \n";
  for (auto& u : itemset.itemSet) {
    Print(u);
  }
}

bool isequal(ItemSet& itemset1, ItemSet& itemset2) {
  if (itemset1.itemSet.size() != itemset2.itemSet.size()) {
    return false;
  } else {
    set<pair<int, int>> core1;
    set<pair<int, int>> core2;

    for (auto& u : itemset1.itemSet) {
      core1.insert({u.productionrInt, u.dot_positionInt});
    }
    for (auto& u : itemset2.itemSet) {
      core2.insert({u.productionrInt, u.dot_positionInt});
    }
    if (core1 == core2) {
      return true;
    } else {
      return false;
    }
  }
}

ItemSet merge(ItemSet& itemset1, ItemSet& itemset2) {
  ItemSet itemset12;
  itemset12.stateInt = itemset1.stateInt;
  for (auto& u : itemset1.itemSet) {
    int a = u.dot_positionInt;
    int b = u.productionrInt;

    for (auto& v : itemset2.itemSet) {
      if (v.dot_positionInt == a && v.productionrInt == b) {
        Item tempitem;
        tempitem.dot_positionInt = a;
        tempitem.productionrInt = b;
        tempitem.prediction.insert(v.prediction.begin(), v.prediction.end());
        tempitem.prediction.insert(u.prediction.begin(),
                                u.prediction.end()); 
        itemset12.itemSet.push_back(tempitem);
      }
    }
  }

  itemset12.edgeMap.insert(itemset1.edgeMap.begin(), itemset1.edgeMap.end());
  itemset12.edgeMap.insert(itemset2.edgeMap.begin(),
                      itemset2.edgeMap.end()); 

  return itemset12;
}

//将 LA1 DFA 转换为 LALR DFA
void LR1ToLALR(Collection& LRcollection, Collection& LALRcollection) {
  // 记录所有具有相同核心的哈希函数
  vector<vector<int>> hash_index;
  for (auto& u : LRcollection) {
    bool flag = true;
    for (auto& v : hash_index) {
      if (v.size() > 0) {
        if (isequal(LRcollection[v[0]], u)) {
          v.push_back(u.stateInt);
          flag = false;
          break;
        }
      }
    }
    if (flag) {
      hash_index.push_back(vector<int>{u.stateInt});
    }
  }

  // 创建哈希映射，将旧 stateInt 映射到新的 stateInt
  map<int, int> hmap;

  int k = 0;
  for (int j = 0; j < hash_index.size(); j++) {
    ItemSet tempIS;
    if (hash_index[j].size() > 1) {
      tempIS = merge(LRcollection[hash_index[j][0]],
                                      LRcollection[hash_index[j][1]]);
      hmap.insert({LRcollection[hash_index[j][0]].stateInt, k});
      hmap.insert({LRcollection[hash_index[j][1]].stateInt, k});
      for (int i = 2; i < hash_index[j].size(); i++) {
        tempIS = merge(LRcollection[hash_index[j][i]], tempIS);
        hmap.insert({LRcollection[hash_index[j][i]].stateInt, k});
      }
      tempIS.stateInt = k;
    } else {
      if (hash_index[j].size() == 1) {
        tempIS = LRcollection[hash_index[j][0]];
        hmap.insert({LRcollection[hash_index[j][0]].stateInt, k});
        tempIS.stateInt = k;
      }
    }
    if (hash_index[j].size() > 0) {
      LALRcollection.push_back(tempIS);
      k++;
    }
  }
  for (auto& u : LALRcollection) {
    for (auto& v : u.edgeMap) {
      u.edgeMap[v.first] = hmap[v.second];
    }
  }
}

void LR1ToTable(Collection& LRcollection, Parse_Table& Parsing_table) {
  // 初始化解析表
  unordered_map<int, int> temp;
  for (int j = 0; j < GlobalSymbolVec.size(); j++) {
    temp.insert({j, INT_MAX});  // error
  }
  for (int i = 0; i < LRcollection.size(); i++) {
    Parsing_table.insert({i, temp});
  }

  for (auto& u : LRcollection) {
    for (auto& v : u.itemSet) {
      if (GlobalProductionVec[v.productionrInt].second.size() ==
          v.dot_positionInt) {
        for (auto& k : v.prediction) {
          Parsing_table[u.stateInt][k] = -v.productionrInt;
        }
        if (GlobalProductionVec[v.productionrInt].first == "S'" &&
            v.productionrInt == GlobalProductionVec.size() - 1) {
          int j;
          for (j = 0; j < GlobalSymbolVec.size(); j++) {
            if (GlobalSymbolVec[j].symbol == "$r") break;
          }
          Parsing_table[u.stateInt][j] = -INT_MAX;
        }
      } else {
      }
    }
    for (auto& v : u.edgeMap) {
      Parsing_table[u.stateInt][v.first] = v.second;
    }
  }
}

void Print_ParsingTable2(Parse_Table& Parsing_table, string filename) {
  fstream output(filename, ios::out);
  output << "State:" << ',';
  // 打印所有终结符号和非终结符号
  int i;
  for (i = 0; i < GlobalSymbolVec.size() - 1; i++) {
    if (GlobalSymbolVec[i].symbol != ",")
      output << GlobalSymbolVec[i].symbol << ',';
    else {
      output << "\",\"" << ',';
    }
  }
  output << GlobalSymbolVec[i].symbol << '\n';

  //打印每个状态
  for (i = 0; i < Parsing_table.size(); i++) {
    output << i << ',';
    int j = 0;
    for (j = 0; j < Parsing_table[i].size() - 1; j++) {
      if (Parsing_table[i][j] > 0) {
        if (Parsing_table[i][j] != INT_MAX) {
          if (GlobalSymbolVec[j].isTerminal)
            output << "S" << Parsing_table[i][j] << ',';
          else {
            output << Parsing_table[i][j] << ',';
          }
        } else {
          output << " " << ',';
        }
      }
      if (Parsing_table[i][j] <= 0) {
        if (Parsing_table[i][j] != -INT_MAX)
          output << "r" << -Parsing_table[i][j] << ',';
        else {
          output << "acc" << ',';
        }
      }
    }

    if (Parsing_table[i][j] > 0) {
      if (Parsing_table[i][j] != INT_MAX) {
        if (GlobalSymbolVec[j].isTerminal)
          output << "S" << Parsing_table[i][j] << '\n';
        else {
          output << Parsing_table[i][j] << '\n';
        }
      } else {
        output << " " << '\n';
      }
    }

    if (Parsing_table[i][j] <= 0) {
      if (Parsing_table[i][j] != -INT_MAX)
        output << "r" << -Parsing_table[i][j] << '\n';
      else {
        output << "acc" << '\n';
      }
    }
  }
}
#endif
