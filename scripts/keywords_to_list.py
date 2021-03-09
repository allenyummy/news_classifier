# Load TXT keywords file to python list.

def main(fn):
    keywords = []
    # encoding = utf-8-sig to remove BOM header
    with open(fn, 'r', encoding='utf-8-sig') as txtfile:
        lines = txtfile.readlines()
        for line in lines:
            word = line.strip()
            keywords.append(word)

    # Print as list
    print("# {} keywords loaded".format(len(keywords)))
    print("# Examples:", keywords[:5])

    #print(keywords)
    # 每10個 一行, 方便閱讀...
    print("[")
    wc = 0
    for w in keywords:
        wc += 1
        if wc % 10 == 0:
            print("'{}',".format(w))
        else:
            print("'{}',".format(w), end = " ")
    print()

if __name__ == '__main__':
    nn_keywords = r'docs/NN_keywords.txt'
    main(nn_keywords)