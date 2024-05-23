#include<iostream>
#include<fstream>
#include<cstdlib>
#include<cstdio>
#include<string>
#include<map>
#include<vector>

using namespace std;

struct Parser
{
    vector<string>terminal;/* data */
	string start;
	using Producer=pair<string, vector<string>>;
	vector< Producer>producer_list;
	std::string program2;
    
    
};
