#include <stdio.h>

int max_with_branch_c(int left, int right) {
    if (left > right) {
        return left;
    }
    return right;
}

int main(void) {
    printf("%d\n", max_with_branch_c(7, 3));
    return 0;
}
