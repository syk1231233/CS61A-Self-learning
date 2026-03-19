#include <cstdio>
#include <iostream>
#include <cmath>
using namespace std;
int z=3;
int f(int &x,int y,int &z){
    x+=y;
    y=x*z;
    z++;
    cout <<x<<' '<< y<<" "<<z<<' ';
    return 0;
}
int main(){
    int x=1,y=3,z=2;
    f(x,y,z);
    cout <<x<<' '<< y<<" "<<::z<<' ';
    f(y,z,x);
    cout <<x<<' '<< y<<" "<<::z<<' ';
    f(z,x,y);
    cout <<x<<' '<< y<<" "<<::z<<' ';
    return 0;
}