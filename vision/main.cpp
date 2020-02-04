#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    Mat img;
    img = imread("../imgs/cntrs.jpg");
    resize(img, img, Size(), 0.2, 0.2, INTER_AREA);

    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", img);

    waitKey(0);

    return 0;
}
