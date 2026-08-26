#include <stdio.h>

int loop_sum_c(int values[], int length) {
    int total = 0;
    for (int index = 0; index < length; index++) {
        total += values[index];
    }
    return total;
}

int main(void) {
    int values[] = {1, 2, 3, 4};
    printf("%d\n", loop_sum_c(values, 4));
    return 0;
}
