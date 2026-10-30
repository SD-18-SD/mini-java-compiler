#include "tac.h"
#include <stdarg.h>

static int temp_count = 1;
static int label_count = 1;

typedef struct TACNode {
    char *code;
    struct TACNode *next;
} TACNode;

static TACNode *head = NULL;
static TACNode *tail = NULL;

char *new_temp(void) {
    char buf[32];
    snprintf(buf, sizeof(buf), "t%d", temp_count++);
    return strdup(buf);
}

char *new_label(void) {
    char buf[32];
    snprintf(buf, sizeof(buf), "L%d", label_count++);
    return strdup(buf);
}

void emit(const char *fmt, ...) {
    char buffer[256];
    va_list args;
    va_start(args, fmt);
    vsnprintf(buffer, sizeof(buffer), fmt, args);
    va_end(args);

    TACNode *node = (TACNode *)malloc(sizeof(TACNode));
    node->code = strdup(buffer);
    node->next = NULL;

    if (head == NULL) {
        head = node;
        tail = node;
    } else {
        tail->next = node;
        tail = node;
    }
}

void print_tac(void) {
    printf("=== THREE-ADDRESS CODE (TAC) ===\n");
    TACNode *curr = head;
    while (curr != NULL) {
        printf("%s\n", curr->code);
        curr = curr->next;
    }
    printf("================================\n\n");
}