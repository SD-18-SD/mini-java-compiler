%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"

extern void yyerror(const char *s);
%}

%option noyywrap
%option yylineno

%%

[ \t\r]+                ; /* Skip whitespace */
\n                      ;

"class"                 { return CLASS; }
"public"                { return PUBLIC; }
"static"                { return STATIC; }
"void"                  { return VOID; }
"main"                  { return MAIN; }
"String"                { return STRING_TYPE; }
"int"                   { int l = yyleng; return INT; }
"float"                 { return FLOAT_TYPE; }
"boolean"               { return BOOLEAN; }
"if"                    { return IF; }
"else"                  { return ELSE; }
"while"                 { return WHILE; }
"return"                { return RETURN; }
"System.out.println"    { return PRINTLN; }
"System.out.print"      { return PRINT; }
"Scanner"               { return SCANNER; }
"System"                { return SYSTEM; }
"in"                    { return IN; }
"nextInt"               { return NEXTINT; }
"nextFloat"             { return NEXTFLOAT; }
"nextLine"              { return NEXTLINE; }
"next"                  { return NEXT; }
"new"                   { return NEW; }
"true"                  { yylval.sval = strdup(yytext); return TRUE; }
"false"                 { yylval.sval = strdup(yytext); return FALSE; }

\"[^\"]*\"              { yylval.sval = strdup(yytext); return STRING_LITERAL; }

[a-zA-Z_][a-zA-Z0-9_]*  { yylval.sval = strdup(yytext); return ID; }
[0-9]+(\.[0-9]+)?       { yylval.sval = strdup(yytext); return NUM; }

"="                     { return ASSIGN; }
"+"                     { return PLUS; }
"-"                     { return MINUS; }
"*"                     { return MULT; }
"/"                     { return DIV; }
">"                     { return GT; }
"<"                     { return LT; }
"=="                    { return EQ; }
"&&"                    { return AND; }
"."                     { return DOT; }

"{"                     { return LBRACE; }
"}"                     { return RBRACE; }
"("                     { return LPAREN; }
")"                     { return RPAREN; }
"["                     { return LBRACK; }
"]"                     { return RBRACK; }
";"                     { return SEMICOLON; }
","                     { return COMMA; }

.                       { }

%%