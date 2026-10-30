#ifndef TAC_H
#define TAC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *new_temp(void);
char *new_label(void);
void emit(const char *fmt, ...);
void print_tac(void);

#endif