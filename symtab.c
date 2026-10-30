#include "symtab.h"

#define TABLE_SIZE 101

static Symbol *hash_table[TABLE_SIZE];
static int current_scope = 0;

static unsigned int hash(const char *str) {
    unsigned int hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % TABLE_SIZE;
}

void init_symtab(void) {
    for (int i = 0; i < TABLE_SIZE; i++) {
        hash_table[i] = NULL;
    }
}

void push_scope(void) {
    current_scope++;
}

void pop_scope(void) {
    for (int i = 0; i < TABLE_SIZE; i++) {
        Symbol *curr = hash_table[i];
        Symbol *prev = NULL;
        while (curr != NULL) {
            if (curr->scope_level == current_scope) {
                Symbol *temp = curr;
                if (prev == NULL) {
                    hash_table[i] = curr->next;
                    curr = hash_table[i];
                } else {
                    prev->next = curr->next;
                    curr = curr->next;
                }
                free(temp->name);
                free(temp->type);
                free(temp);
            } else {
                prev = curr;
                curr = curr->next;
            }
        }
    }
    if (current_scope > 0) {
        current_scope--;
    }
}

int insert_symbol(const char *name, const char *type, int line) {
    unsigned int idx = hash(name);
    Symbol *curr = hash_table[idx];
    
    while (curr != NULL) {
        if (strcmp(curr->name, name) == 0 && curr->scope_level == current_scope) {
            fprintf(stderr, "Semantic Error at line %d: Redeclaration of identifier '%s'\n", line, name);
            return 0;
        }
        curr = curr->next;
    }

    Symbol *new_sym = (Symbol *)malloc(sizeof(Symbol));
    new_sym->name = strdup(name);
    new_sym->type = strdup(type);
    new_sym->line = line;
    new_sym->scope_level = current_scope;
    new_sym->next = hash_table[idx];
    hash_table[idx] = new_sym;

    return 1;
}

Symbol *lookup_symbol(const char *name) {
    unsigned int idx = hash(name);
    Symbol *curr = hash_table[idx];
    
    Symbol *best_match = NULL;
    int highest_scope = -1;

    while (curr != NULL) {
        if (strcmp(curr->name, name) == 0) {
            if (curr->scope_level > highest_scope) {
                highest_scope = curr->scope_level;
                best_match = curr;
            }
        }
        curr = curr->next;
    }
    return best_match;
}

void print_symbol_table(void) {
    printf("\n=== SYMBOL TABLE ===\n");
    printf("%-15s | %-10s | %-5s\n", "Identifier", "Type", "Line");
    printf("-----------------------------------\n");
    for (int i = 0; i < TABLE_SIZE; i++) {
        Symbol *curr = hash_table[i];
        while (curr != NULL) {
            printf("%-15s | %-10s | %-5d\n", curr->name, curr->type, curr->line);
            curr = curr->next;
        }
    }
    printf("====================\n\n");
}