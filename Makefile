CC = gcc
CFLAGS = -Wall -g
LEX = win_flex
YACC = win_bison -d

OBJS = lex.yy.o parser.tab.o symtab.o tac.o

all: compiler.exe

compiler.exe: $(OBJS)
	$(CC) $(CFLAGS) -o compiler.exe $(OBJS)

lex.yy.c: lexer.l parser.tab.h
	$(LEX) lexer.l

parser.tab.c parser.tab.h: parser.y
	$(YACC) parser.y

symtab.o: symtab.c symtab.h
	$(CC) $(CFLAGS) -c symtab.c

tac.o: tac.c tac.h
	$(CC) $(CFLAGS) -c tac.c

clean:
	del /f /q *.o lex.yy.c parser.tab.c parser.tab.h $(TARGET)