#include <iostream>
#include "tttBoard.h"
#include <opencv2/opencv.hpp>

using namespace cv;

void get_checkers_board(Mat const& img){
    Mat corners;
    if( findChessboardCorners(img, Size2i(7,7), corners) )
        corners = corners.reshape(0, 7);
    else
        return;

    Mat extend = Mat::zeros(9,9, corners.type());
    copyMakeBorder(corners, extend, 1, 1, 1, 1, BORDER_ISOLATED);

    for (int row = 1; row < 8; ++row){
        extend.row(row).col(0) = 2 * extend.row(row).col(1) - extend.row(row).col(2);
        extend.row(row).col(8) = 2 * extend.row(row).col(7) - extend.row(row).col(6);
    }

    extend.row(0) = 2 * extend.row(1) - extend.row(2);
    extend.row(8) = 2 * extend.row(7) - extend.row(6);
}

int main() {

    tttBoard board;

    Board representation
    {3, std::vector<player_type>(3, NONE)};



//    Mat img;
//    img = imread("../imgs/cntrs.jpg");
//    resize(img, img, Size(), 0.2, 0.2, INTER_AREA);
//
//    get_checkers_board(img);
//
//    namedWindow("Display Image", WINDOW_AUTOSIZE);
//    imshow("Display Image", img);
//
//    waitKey(0);

    return 0;
}