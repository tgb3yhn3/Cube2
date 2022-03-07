#include<iostream>
#include<stdio.h>
#include<math.h>
#include<vector>
#include<graphics.h>
#include <stdlib.h> /* 亂數相關函數 */
#include <time.h>   /* 時間相關函數 */

using namespace std;
class cube {
private:
    /// <summary>
    /// 白0、黃1、橙2、紅3、綠4、藍5
    /// </summary>

    friend ostream& operator<<(ostream&, const cube&);
public:
    int cubeFace[6][3][3];
    cube() {//初始化 預設所有面原本的顏色
        srand(time(NULL));

        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 3; j++) {
                for (int k = 0; k < 3; k++) {
                    cubeFace[i][j][k] =i;
                }
            }
        }
        rotation_clockwise(2);
        rotation_clockwise(2);
        rotation_clockwise(2);
        rotation_clockwise(2);
        rotation_counterclockwise(2);

    }
    void setCubeFace(int cubeFace[6][3][3]) {//設定整個魔術方塊每一面的顏色
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 3; j++) {
                for (int k = 0; k < 3; k++) {
                    this->cubeFace[i][j][k] = cubeFace[i][j][k];
                }
            }
        }
    }
    void showInCh() {
        const char* dict[6] = { "白" ,"黃","橙","紅","綠","藍" };
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 3; j++) {
                for (int k = 0; k < 3; k++) {
                    cout << dict[cubeFace[i][j][k]] << " ";
                }
                cout << endl;
            }
            cout << "-------------" << endl;
        }
    }
    void swap(int&a,int&b) {
        int temp = a;
        a = b;
        b = temp;
    }
    void rotation_clockwise(int faceNum) {//順時針旋轉
        switch (faceNum) {//faceNum為第幾面

        case 2:
            swap(cubeFace[1][0][2], cubeFace[0][2][2]);
            swap(cubeFace[1][1][2], cubeFace[0][2][1]);
            swap(cubeFace[1][2][2], cubeFace[0][2][0]);

            swap(cubeFace[1][0][2], cubeFace[3][2][0]);
            swap(cubeFace[1][1][2], cubeFace[3][1][0]);
            swap(cubeFace[1][2][2], cubeFace[3][0][0]);

            swap(cubeFace[1][0][2], cubeFace[5][0][0]);
            swap(cubeFace[1][1][2], cubeFace[5][0][1]);
            swap(cubeFace[1][2][2], cubeFace[5][0][2]);
        }
    }
    void rotation_counterclockwise(int faceNum) {//逆時針旋轉
        switch (faceNum) {//faceNum為第幾面

        case 2:
            swap(cubeFace[1][0][2], cubeFace[5][0][0]);
            swap(cubeFace[1][1][2], cubeFace[5][0][1]);
            swap(cubeFace[1][2][2], cubeFace[5][0][2]);

            swap(cubeFace[1][0][2], cubeFace[3][2][0]);
            swap(cubeFace[1][1][2], cubeFace[3][1][0]);
            swap(cubeFace[1][2][2], cubeFace[3][0][0]);

            swap(cubeFace[1][0][2], cubeFace[0][2][2]);
            swap(cubeFace[1][1][2], cubeFace[0][2][1]);
            swap(cubeFace[1][2][2], cubeFace[0][2][0]);           
        }
    }


};
ostream& operator<<(ostream& os, const cube& cube)
{
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 3; j++) {
            for (int k = 0; k < 3; k++) {
                os << cube.cubeFace[i][j][k] << " ";
            }
            os << "\n";
        }
        os << "--------------" << "\n";
    }
    return os;
}
void show(cube c) {
    const int blockH = 30;
    initgraph(500, 500); // 初始化640 * 480大小的窗口 // 添加繪圖邏輯​​

    //rectangle(10, 10, 40, 40); // 畫矩形​
    //fillrectangle 用顏色畫矩形
    while (true) {
        for (int i = 0; i < 6; i++) {
        }
            for (int j = 0; j < 3; j++) {
                for (int k = 0; k < 3; k++) {
                    switch (c.cubeFace[0][j][k])
                    {
                        /// 白0、黃1、橙2、紅3、綠4、藍5
                    case 0:
                        setfillcolor(0xd0d0d0);
                        break;
                    case 1:
                        setfillcolor(YELLOW);
                        break;
                    case 2:
                        setfillcolor(0x00a5ff);
                        break;
                    case 3:
                        setfillcolor(RED);
                        break;
                    case 4:
                        setfillcolor(GREEN);
                        break;
                    case 5:
                        setfillcolor(BLUE);
                        break;
                    default:
                        setfillcolor(WHITE);
                    }
                    fillrectangle(k * 30+90,  j * 30, k * 30 + 120,  j * 30 + 30);
                }
            }
            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 3; j++) {
                    for (int k = 0; k < 3; k++) {
                        switch (c.cubeFace[i+1][j][k])
                        {
                            /// 白0、黃1、橙2、紅3、綠4、藍5
                        case 0:
                            setfillcolor(0xd0d0d0);
                            break;
                        case 1:
                            setfillcolor(YELLOW);
                            break;
                        case 2:
                            setfillcolor(0x00a5ff);
                            break;
                        case 3:
                            setfillcolor(RED);
                            break;
                        case 4:
                            setfillcolor(GREEN);
                            break;
                        case 5:
                            setfillcolor(BLUE);
                            break;
                        default:
                            setfillcolor(WHITE);
                        }
                        fillrectangle(k * 30 + i*90, j * 30+90, k * 30 + i * 90 + 30, j * 30 + 120);
                    }
                    cout << endl;
                }
            }
            for (int j = 0; j < 3; j++) {
                for (int k = 0; k < 3; k++) {
                    switch (c.cubeFace[5][j][k])
                    {
                        /// 白0、黃1、橙2、紅3、綠4、藍5
                    case 0:
                        setfillcolor(0xd0d0d0);
                        break;
                    case 1:
                        setfillcolor(YELLOW);
                        break;
                    case 2:
                        setfillcolor(0x00a5ff);
                        break;
                    case 3:
                        setfillcolor(RED);
                        break;
                    case 4:
                        setfillcolor(GREEN);
                        break;
                    case 5:
                        setfillcolor(BLUE);
                        break;
                    default:
                        setfillcolor(WHITE);
                    }
                    fillrectangle(k * 30 + 90, j * 30 + 180, k * 30 +120 , j * 30 + 210);
                }
                cout << endl;
            }
    }
}
void test() {
    const int blockH = 30;
    initgraph(640, 480); // 初始化640 * 480大小的窗口 // 添加繪圖邏輯​​
    while (true) {
        //x橫 起始點 Y起始點，往x延伸多少，往y延伸多少
        setfillcolor(BLUE);
        fillrectangle(0, 300, 50, 400);
            

            Sleep(1);
        
    }
}
int main(void) {
    cube* a = new cube();
   show(*a);
   
    //test();
   
    cout << *a;
    a->showInCh();
    cout << "YA";
}