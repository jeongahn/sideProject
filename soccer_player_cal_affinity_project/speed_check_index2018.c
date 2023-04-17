#include <stdio.h>
#include <time.h>

int main()
{
    clock_t start, end;
    double result;

    start = clock();
    system("index2018.exe combined_KMA_949.txt");
    end = clock();

    result = (double)(end - start) / CLOCKS_PER_SEC;
    printf("실행 시간: %lf초\n", result);

    return 0;
}
