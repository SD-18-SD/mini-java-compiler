code = r"""%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symtab.h"
#include "tac.h"

extern int yylex();
extern int yylineno;
extern FILE *yyin;

int line_num = 1;
void print_symtab();
void print_tac();

void yyerror(const char *s) {
    fprintf(stderr, "Syntax Error at line %d: %s\n", yylineno, s);
}
%}

%union {
    int ival;
    char *sval;
}

%token CLASS PUBLIC STATIC VOID MAIN STRING_TYPE INT BOOLEAN
%token IF ELSE WHILE RETURN PRINTLN TRUE FALSE COMMA
%token SCANNER SYSTEM IN NEXTINT NEW DOT
%token <sval> ID
%token <ival> NUM
%token ASSIGN PLUS MINUS MULT DIV GT LT EQ AND
%token LBRACE RBRACE LPAREN RPAREN LBRACK RBRACK SEMICOLON

%type <sval> expr

%left AND
%left EQ
%left GT LT
%left PLUS MINUS
%left MULT DIV

%%

program:
    class_decl
    ;

class_decl:
    CLASS ID LBRACE main_method method_list RBRACE
    ;

main_method:
    PUBLIC STATIC VOID MAIN LPAREN STRING_TYPE LBRACK RBRACK ID RPAREN LBRACE statements RBRACE
    ;

method_list:
    method_decl method_list
    | /* empty */
    ;

method_decl:
    PUBLIC INT ID LPAREN param_list RPAREN LBRACE statements RETURN expr SEMICOLON RBRACE {
        emit("return", $10, "", "");
    }
    ;

param_list:
    type ID param_tail
    | /* empty */
    ;

param_tail:
    COMMA type ID param_tail
    | /* empty */
    ;

type:
    INT LBRACK RBRACK
    | BOOLEAN
    | INT
    | SCANNER
    ;

statements:
    statement statements
    | /* empty */
    ;

statement:
    var_decl
    | assign_stmt
    | array_assign_stmt
    | if_stmt
    | while_stmt
    | print_stmt
    ;

var_decl:
    INT ID SEMICOLON {
        line_num = yylineno;
        insert_symbol($2, "int", yylineno);
    }
    | INT LBRACK RBRACK ID SEMICOLON {
        line_num = yylineno;
        insert_symbol($4, "int[]", yylineno);
    }
    | BOOLEAN ID SEMICOLON {
        line_num = yylineno;
        insert_symbol($2, "boolean", yylineno);
    }
    | SCANNER ID SEMICOLON {
        line_num = yylineno;
        insert_symbol($2, "Scanner", yylineno);
    }
    ;

assign_stmt:
    ID ASSIGN expr SEMICOLON {
        if (lookup_symbol($1) == NULL) {
            printf("Semantic Error at line %d: Variable '%s' undeclared!\n", yylineno, $1);
        } else {
            emit($1, $3, "", "=");
        }
    }
    ;

array_assign_stmt:
    ID LBRACK expr RBRACK ASSIGN expr SEMICOLON {
        char index_expr[64];
        sprintf(index_expr, "%s[%s]", $1, $3);
        emit(index_expr, $6, "", "=");
    }
    ;

if_stmt:
    IF LPAREN expr RPAREN {
        char *label1 = new_label();
        emit("ifFalse", $3, "goto", label1);
        $<sval>$ = label1;
    } LBRACE statements RBRACE {
        char *label2 = new_label();
        emit("goto", label2, "", "");
        emit($<sval>5, "", "", "LABEL");
        $<sval>$ = label2;
    } ELSE LBRACE statements RBRACE {
        emit($<sval>9, "", "", "LABEL");
    }
    ;

while_stmt:
    WHILE {
        char *start_label = new_label();
        emit(start_label, "", "", "LABEL");
        $<sval>$ = start_label;
    } LPAREN expr RPAREN {
        char *end_label = new_label();
        emit("ifFalse", $4, "goto", end_label);
        $<sval>$ = end_label;
    } LBRACE statements RBRACE {
        emit("goto", $<sval>2, "", "");
        emit($<sval>6, "", "", "LABEL");
    }
    ;

print_stmt:
    PRINTLN LPAREN expr RPAREN SEMICOLON {
        emit("print", $3, "", "");
    }
    ;

expr:
    expr PLUS expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "+");
        $$ = temp;
    }
    | expr MINUS expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "-");
        $$ = temp;
    }
    | expr MULT expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "*");
        $$ = temp;
    }
    | expr DIV expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "/");
        $$ = temp;
    }
    | expr GT expr {
        char *temp = new_temp();
        emit(temp, $1, $3, ">");
        $$ = temp;
    }
    | expr LT expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "<");
        $$ = temp;
    }
    | expr EQ expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "==");
        $$ = temp;
    }
    | expr AND expr {
        char *temp = new_temp();
        emit(temp, $1, $3, "&&");
        $$ = temp;
    }
    | NEW SCANNER LPAREN SYSTEM DOT IN RPAREN {
        $$ = strdup("new_scanner()");
    }
    | ID DOT NEXTINT LPAREN RPAREN {
        char *temp = new_temp();
        emit(temp, "read()", "", "=");
        $$ = temp;
    }
    | ID LBRACK expr RBRACK {
        char *temp = new_temp();
        char index_expr[64];
        sprintf(index_expr, "%s[%s]", $1, $3);
        emit(temp, index_expr, "", "=");
        $$ = temp;
    }
    | ID {
        if (lookup_symbol($1) == NULL) {
            printf("Semantic Error at line %d: Variable '%s' undeclared!\n", yylineno, $1);
        }
        $$ = $1;
    }
    | NUM {
        char str[16];
        sprintf(str, "%d", $1);
        $$ = strdup(str);
    }
    | TRUE { $$ = strdup("true"); }
    | FALSE { $$ = strdup("false"); }
    ;

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error opening input file");
            return 1;
        }
        yyin = file;
    } else {
        printf("Usage: %s <source_file.java>\n", argv[0]);
        return 1;
    }

    init_symtab();
    yyparse();
    print_tac(); // print_tac handles its own clean formatting headers

    return 0;
}
"""

with open("parser.y", "w", encoding="utf-8") as f:
    f.write(code)
print("parser.y cleaned up!")
