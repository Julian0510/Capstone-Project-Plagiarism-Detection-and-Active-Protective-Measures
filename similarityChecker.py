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

    # # reading the file
    # with open(filename1) as fp:
    #     contents1 = fp.read()

    # with open(filename2) as fp:
    #     contents2 = fp.read()

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
    # contents1 = contents1.replace("\\s", "")
    # contents2 = contents2.replace("\\s", "")
    contents1 = re.sub("\\s", "", contents1)
    contents2 = re.sub("\\s", "", contents2)

    # print(name1, ":", contents1)
    # print(name2, ":", contents2)
    # # code for testing purposes
    # with open("newfile.java", "w") as fp:
    #     fp.writelines(contents1)
    # with open("newfile2.java", "w") as fp:
    #     fp.writelines(contents2)

    # Compute the Levenshtein distance
    similarityScore = abs((1 - levenshtein_distance(contents1,
                          contents2) / min(len(contents1), len(contents2)))) * 100
    print("Similarity score is: " + str(similarityScore) + "%")

    # Prints out the result of comparing two files
    if similarityScore == 100:
        print("The two files are identical!")
    elif similarityScore > 70:
        print("There are a lot of similarities between the two files.")
    elif similarityScore > 30:
        print("There are some resemblances between the two files.")
    else:
        print("No worries! There appears to be no sign of plagiarism.")


# Driver code for testing the function
# the zip filenames of the two homework files that we will compare
print("Enter the name of the first file you will be comparing: ")
filename1 = input()
contents1 = openFile(filename1)
file_extension1 = fileExtensionFinder(filename1)

print("Enter the name of the second file you will be comparing: ")
filename2 = input()
contents2 = openFile(filename2)
file_extension2 = fileExtensionFinder(filename2)

# for reading files in zip format. Unused as of now

# zipfile1 = "ElevenToothpicksSubmissions/P1.zip"
# zipfile2 = "ElevenToothpicksSubmissions/W1.zip"

# # reading the contents of zipfile1
# with zipfile.ZipFile(zipfile1, "r") as thezip:
#     files = thezip.namelist()  # should only be 1 file here!
#     file_extension1 = fileExtensionFinder(files[0])
#     with thezip.open(files[0]) as fp:
#         contents1 = fp.read()
#         contents1 = contents1.decode()  # decode the contents to be readable as a str

# # reading the contents of zipfile2
# with zipfile.ZipFile(zipfile2, "r") as thezip:
#     files = thezip.namelist()  # should only be 1 file here!
#     file_extension2 = fileExtensionFinder(files[0])
#     with thezip.open(files[0]) as fp:
#         contents2 = fp.read()
#         contents2 = contents2.decode()  # decode the contents to be readable as a str

if file_extension1 == file_extension2:
    if file_extension1 == ".java":
        similarityChecker(contents1, contents2, keywords_java)
    elif file_extension1 == ".cpp":
        print("C++")
        similarityChecker(contents1, contents2, keywords_cpp)
    else:
        print("Unsupported file type! Only C++ or Java file types supported!")
else:
    raise ValueError(
        "file types are not the same. Please make sure that both files are of the same type")
