#ifndef SYMTAB_H
#define SYMTAB_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Symbol {
    char *name;
    char *type;
    int line;
    int scope_level;
    struct Symbol *next;
} Symbol;

void init_symtab(void);
int insert_symbol(const char *name, const char *type, int line);
Symbol *lookup_symbol(const char *name);
void push_scope(void);
void pop_scope(void);
void print_symbol_table(void);

#endif