try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


# Dynamic Programming implementation of LCS problem
# Function found at https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/
def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in range(m + 1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


# end of function lcs

# a function used to reformat urls to more accurately represent the question statement
def prettify(s: str) -> str:
    # 58 is the length of 'https://www.chegg.com/homework-help/questions-and-answers/'
    # so we want to get the text after this baseurl
    s = s[58:]
    # replace dashs with spaces
    s = s.replace('-', ' ')

    # we need this variable to remove the end id of the url ex. q0000000
    endindex = -100
    for i in range(len(s) - 1, -1, -1):
        if s[i] == 'q':
            endindex = i
            break
    s = s[:endindex]
    return s


# used to reformat the question to a more accurate form to match the chegg url
def reformatQuestion(s: str) -> str:
    # there are a list of stopwords found in stopwords.txt. Stopwords are words that are removed from urls

    removeableWords = stopWords
    punctuation = ['.', ',', '?', '!', ';', ':', '\'', '\"']
    s = s.lower()
    for mark in punctuation:
        s.replace(mark, '')
    for word in removeableWords:
        s = s.replace(f' {word} ', ' ')

    # we return the first 100 characters because that's all that chegg will show in the url
    return s[:100]


# used to load data into a list
def load(file: str) -> list[str]:
    f = open(file, 'r')
    data = []
    for line in f:
        data.append(line[:-1])
    return data


# initialization of variables
stopWords = load('stopwords.txt')
baseurl = 'https://www.chegg.com/homework-help/questions-and-answers/'
site = 'chegg'
output = ''
questions = load('questions.txt')
strongMatchThreshold = 0.75

# Go through every question in the list
for i, question in enumerate(questions):
    output += f'{i + 1}. {question}\n\t'
    # set up the google search query
    query = f"{site} {question}"

    hits = []
    strongMatch = []
    count = 0
    # perform the google search query
    for j in search(query, tld="co.in", num=100, stop=100, pause=2):
        # makes sure that only chegg sites get added
        if j[:len(baseurl)] == baseurl:
            hits.append(j)
        count += 1
    # for every chegg site returned from the query
    for url in hits:
        # reformat the url and the question to be more similar
        urlQuestion = prettify(url)
        question = reformatQuestion(question)

        # take the length of the LCS divided by the length of the question to see how much of the question is in the url
        commonality = lcs(question, urlQuestion) / len(question)

        # if the commonality surpasses a certain threshhold add it to the strongMatch list
        if commonality > strongMatchThreshold:
            strongMatch.append((url, commonality))

    # append strong matches to the output string with the level of confidence
    for match in strongMatch:
        output += f'URL:{match[0]}\n\tConfidence: {match[1]}\n\t'
    output += '\n'
print(output)
