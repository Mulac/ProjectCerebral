#include <iostream>
#include "tttBoard.h"

bool tttBoard::isValidMove(const Board &brd) {
    int diff_count = 0;

    for (int i = 0; i < board.size(); ++i)
        for (int j = 0; j < board.size(); ++j)
            if (brd.at(i).at(j) != board.at(i).at(j)) {     // Find the differences
                // Make sure only 1 difference with the correct player choosing empty position
                if (diff_count > 0 || board.at(i).at(j) != NONE || brd.at(i).at(j) != nextPlayer())
                    return false;
                diff_count++;
            }

    if (diff_count == 1){
        updateBoard(brd);
        return true;
    } else return false;
}


bool tttBoard::isEnd() {
    if (board.at(1).at(1) != NONE)  // Check the two diagonals
        if ((board.at(0).at(0) == board.at(1).at(1) && board.at(1).at(1) == board.at(2).at(2)) ||
            (board.at(0).at(2) == board.at(1).at(1) && board.at(1).at(1) == board.at(2).at(0)))
            return true;

    for (int i = 0; i < board.size(); ++i)  // Check the 6 straight lines
        if (board.at(i).at(i) != NONE)
            if ((board.at(i).at(0) == board.at(i).at(1) && board.at(i).at(1) == board.at(i).at(2)) ||
                    (board.at(0).at(i) == board.at(1).at(i) && board.at(1).at(i) == board.at(2).at(i)))
                return true;

    return move == 9;   // Check for full board
}


void tttBoard::updateBoard(const Board brd) {
    board = brd;
    move++;
}


player_type tttBoard::nextPlayer() {
    if (move % 2 == 0)
        return HUMAN;
    else
        return COMPUTER;
}

int tttBoard::getMove() const {
    return move;
}
