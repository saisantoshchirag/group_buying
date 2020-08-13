#include<stdio.h>
int main()
{
    int arr[10] = {1,2,3,4,5,6,7,8,9,10};
    int n=10;
    int b[n];
    for(int i=0,j=9;i<10,j>=0;i++,j--)
    {
        b[j] = arr[i];

    }
    for(int k=0;k<10;k++){
        printf("%d",b[k]);
    }
    return 0;
}
