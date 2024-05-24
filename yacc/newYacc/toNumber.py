# import re

# class GrammarMapper:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.grammar = self._read_grammar_from_file()
#         self.mapping = {}
#         self.reverse_mapping = {}
#         self.nonterminal_counter = 1
#         self.terminal_counter = -1
#         self._parse_grammar()

#     def _read_grammar_from_file(self):
#         with open(self.file_path, 'r') as file:
#             return file.read()

#     def _parse_grammar(self):
#         # 提取非终结符和终结符
#         nonterminals = set(re.findall(r'\b[a-z_]+\b', self.grammar))
#         terminals = set(re.findall(r'\b[A-Z_]+\b', self.grammar))

#         # 提取标点符号
#         punctuation = set(re.findall(r'[.,(){};]', self.grammar))

#         # 映射非终结符
#         for nonterminal in nonterminals:
#             if nonterminal not in self.mapping:
#                 self.mapping[nonterminal] = self.nonterminal_counter
#                 self.nonterminal_counter += 1

#         # 映射终结符
#         for terminal in terminals:
#             if terminal not in self.mapping:
#                 self.mapping[terminal] = self.terminal_counter
#                 self.terminal_counter -= 1

#         # 映射标点符号
#         for punct in punctuation:
#             if punct not in self.mapping:
#                 self.mapping[punct] = self.terminal_counter
#                 self.terminal_counter -= 1

#         # 生成反向映射
#         self.reverse_mapping = {v: k for k, v in self.mapping.items()}

#     def get_mapping(self):
#         return self.mapping

#     def print_mapping(self):
#         for symbol, number in self.mapping.items():
#             print(f"{number}: {symbol}")

#     def get_symbol_by_number(self, number):
#         return self.reverse_mapping.get(number, None)

#     def get_number_by_symbol(self, symbol):
#         return self.mapping.get(symbol, None)

#     def save_mapping_to_file(self, output_file):
#         with open(output_file, 'w') as file:
#             for symbol, number in self.mapping.items():
#                 file.write(f"{number} {symbol}\n")

# # 创建GrammarMapper对象并生成映射
# file_path = './yacc/newYacc/c99.y'
# output_file = './yacc./newYacc/result.txt'
# mapper = GrammarMapper(file_path)

# # 保存映射结果到文件
# mapper.save_mapping_to_file(output_file)

# # # 测试新增方法
# # test_number = 1
# # test_symbol = 'IDENTIFIER'

# # # 将测试结果写入文件
# # with open(output_file, 'a') as file:
# #     file.write(f"Symbol for number {test_number}: {mapper.get_symbol_by_number(test_number)}\n")
# #     file.write(f"Number for symbol '{test_symbol}': {mapper.get_number_by_symbol(test_symbol)}\n")

# # 打印文件内容（可选）
# # with open(output_file, 'r') as file:
# #     print(file.read())

# 不要运行这个文件
