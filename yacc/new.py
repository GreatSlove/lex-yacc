def extract_last_word(file1):
    """
    从文件1中提取每行的最后一个单词
    """
    last_words = []
    with open(file1, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            if words:  # 确保这一行不为空
                last_words.append(words[-1])
    return last_words

def find_words_in_file(words, file2):
    """
    在文件2中查找每个单词
    """
    with open(file2, 'r', encoding='utf-8') as f:
        file2_contents = f.read()
    
    not_found_words = []
    for word in words:
        if word not in file2_contents:
            not_found_words.append(word)
    
    return not_found_words

def main():
    file1 = './yacc/ina.txt'
    file2 = './yacc/first.txt'
    
    last_words = extract_last_word(file1)
    not_found_words = find_words_in_file(last_words, file2)
    
    if not_found_words:
        print("这些单词没有在文件2中找到:")
        for word in not_found_words:
            print(word)
    else:
        print("所有单词都在文件2中找到了")

if __name__ == "__main__":
    main()
