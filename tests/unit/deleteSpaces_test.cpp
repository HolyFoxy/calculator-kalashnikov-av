#include <gtest/gtest.h>
#include <fcntl.h>
#include <cstdio>
#include <string>

extern "C" {
    char* deleteSpaces();
}

TEST(deleteSpacesTest, SimpleSpaces) {
    const char* exp = "1 + 1  -  2";
    FILE* instream = fmemopen((void*)exp, strlen(exp), "r");
    FILE* t = stdin;
    stdin = instream;
    char* res = deleteSpaces();
    fclose(instream);
    std::string str = "";
    for (int i = 0; i < 5; i++)
        str += res[i];
    EXPECT_EQ("1+1-2", str);
}

TEST(deleteSpacesTest, NOTSimpleSpaces) {
    const char* exp = "1\n+\r1\t\f-  2";
    FILE* instream = fmemopen((void*)exp, strlen(exp), "r");
    FILE* t = stdin;
    stdin = instream;
    char* res = deleteSpaces();
    fclose(instream);
    std::string str = "";
    for (int i = 0; i < 5; i++)
        str += res[i];
    EXPECT_EQ("1+1-2", str);
}
