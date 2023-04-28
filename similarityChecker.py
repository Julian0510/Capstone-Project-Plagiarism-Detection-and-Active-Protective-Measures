from Levenshtein import distance as levenshtein_distance
import zipfile
import re
import pathlib


# Java keywords list
keywords_java = ["public", "void", "private", "boolean", "true",
                 "false", "null", "abstract", "assert", "int", "double", "else",
                 "break", "byte", "case", "catch", "char", "class", "const",
                 "continue", "default", "do", "enum", "extends", "for", "finally",
                 "float", "goto", "if", "implements", "import", "instanceof",
                 "interface", "long", "native", "new", "package", "protected",
                 "return", "short", "static", "strictfp", "super", "switch",
                 "synchronized", "this", "throw", "throws", "transient", "try",
                 "volatile", "while"]

# C++ keywords list
# c++ keywords found here: https://en.cppreference.com/w/cpp/keyword
keywords_cpp = ["alignas", "alignof", "and", "and_eq", "asm",
                "atomic_cancel", "atomic_commit", "atomic_noexcept",
                "auto", "bitland", "bitor", "bool", "break", "case",
                "catch", "char", "char8_t", "char16_t", "char32_t", "class",
                "compl", "concept", "const", "consteval", "constexpr", "constinit",
                "const_cast", "continue", "co_await", "co_return", "co_yield",
                "decltype", "default", "delete", "do", "double", "dynamic_cast",
                "else", "enum", "explicit", "export", "extern", "false", "float",
                "for", "friend", "goto", "if", "inline", "int", "long", "mutable",
                "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator",
                "or", "or_eq", "private", "protected", "public", "reflexpr", "register",
                "reinterpret_cast", "requires", "return", "short", "signed", "sizeof",
                "static", "static_assert", "static_cast", "struct", "switch", "synchronized",
                "template", "this", "thread_local", "throw", "true", "try", "typedef",
                "typeid", "typename", "union", "unsigned", "using", "virtual", "void",
                "volatile", "wchar_t", "while", "xor", "xor_eq"]


def fileExtensionFinder(filename):
    try:
        file_extension = pathlib.Path(filename).suffix
    except:
        print("Error finding the fileextension")
    return file_extension


def openFile(filename):
    try:
        with open(filename) as fp:
            contents = fp.read()
    except:
        print("Unable to read file")

    return contents


def similarityChecker(contents1, contents2, keywords):

    # Remove comments - first in-line comments, next block comments, lastly JavaDoc comments
    contents1 = re.sub("//.*", "", contents1)
    contents1 = re.sub("/\\*.*?\\*/", "", contents1)
    contents1 = re.sub("/\\*\\*(?s:(?!\\*/).)*\\*/", "", contents1)

    contents2 = re.sub("//.*", "", contents2)
    contents2 = re.sub("/\\*.*?\\*/", "", contents2)
    contents2 = re.sub("/\\*\\*(?s:(?!\\*/).)*\\*/", "", contents2)

    contentsArray = contents1.split()
    contentsArray2 = contents2.split()

    # remove all keywords in both input text files
    for i in range(0, len(contentsArray)):
        if contentsArray[i] in keywords:
            contents1 = contents1.replace(contentsArray[i], "")

    for i in range(0, len(contentsArray2)):
        if contentsArray2[i] in keywords:
            contents2 = contents2.replace(contentsArray2[i], "")

    # Remove whitespace and tabs
    contents1 = re.sub("\\s", "", contents1)
    contents2 = re.sub("\\s", "", contents2)

    # # code for testing purposes
    # print(name1, ":", contents1)
    # print(name2, ":", contents2)
    # with open("newfile.java", "w") as fp:
    #     fp.writelines(contents1)
    # with open("newfile2.java", "w") as fp:
    #     fp.writelines(contents2)

    # Compute the Levenshtein distance
    similarityScore = abs((1 - levenshtein_distance(contents1,
                          contents2) / min(len(contents1), len(contents2)))) * 100
    similarityScore = float('%.2f' % (similarityScore))
    #print("Similarity score is: " + str(similarityScore) + "%")

    # # Prints out the result of comparing two files
    # if similarityScore == 100:
    #     print("The two files are identical!")
    # elif similarityScore > 70:
    #     print("There are a lot of similarities between the two files.")
    # elif similarityScore > 30:
    #     print("There are some resemblances between the two files.")
    # else:
    #     print("No worries! There appears to be no sign of plagiarism.")

    return similarityScore


# Driver code for testing the function

# the name of the zipfile that has all of the homework solutions we will be comparing
zipfile1 = "ElevenToothpicksSubmissions.zip"


# reading the contents of zipfile1
with zipfile.ZipFile(zipfile1, "r") as thezip:
    files = thezip.namelist()

    all_info = []
    for file in files:
        temp_info = []
        # get the file name without the entire path variable
        filename = file.split("/")[-1]
        temp_info.append(filename)

        with zipfile.ZipFile(file, "r") as z:
            contents_list = z.namelist()  # should only be one!
            file_extension = fileExtensionFinder(contents_list[0])

            with z.open(contents_list[0]) as fp:
                contents = fp.read()
                contents = contents.decode()  # decode the contents to be readable as a str

                temp_info.append(contents)
                temp_info.append(file_extension)

        all_info.append(temp_info)

# # for testing
# for i in range(0, len(all_info)):
#     print(all_info[i][0])  # filenames should be printed


similarityScores = []

for i in range(0, len(all_info)):
    target_file = all_info[i]
    file_extension1 = all_info[i][2]
    contents1 = all_info[i][1]
    simiScores_main = []
    simiScores_main.append(all_info[i][0])
    for k in range(0, len(all_info)):
        # check to make sure we don't compare the same file with itself
        if all_info[k][0] == all_info[i][0]:
            continue
        else:
            file_extension2 = all_info[k][2]

            if file_extension1 == file_extension2:
                simiScores_temp = []
                simiScores_temp.append(all_info[k][0])

                if file_extension1 == ".java":
                    contents2 = all_info[k][1]
                    similarityScore = similarityChecker(
                        contents1, contents2, keywords_java)
                    simiScores_temp.append(similarityScore)
                elif file_extension1 == ".cpp":
                    contents2 = all_info[k][1]
                    similarityScore = similarityChecker(
                        contents1, contents2, keywords_cpp)
                    simiScores_temp.append(similarityScore)
                else:
                    print(
                        "Unsupported file type! Only C++ or Java file types supported!")
            else:
                raise ValueError(
                    "file types are not the same. Please make sure that both files are of the same type")

            simiScores_main.append(simiScores_temp)

    similarityScores.append(simiScores_main)


for i in range(0, len(similarityScores)):
    print("Here is a list of files that were flagged as similar to",
          similarityScores[i][0], ":")
    for k in range(0, len(similarityScores[i])):
        if float(similarityScores[i][k][1]) >= 70.0:
            print("\t", similarityScores[i][k][0],
                  "had a similarity score of:", similarityScores[i][k][1], "%")

    print("")
