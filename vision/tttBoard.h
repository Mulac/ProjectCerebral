#ifndef VISION_TTTBOARD_H
#define VISION_TTTBOARD_H

#include <vector>

typedef enum {NONE, COMPUTER, HUMAN} player_type;
typedef std::vector<std::vector<player_type>> Board;

class tttBoard {
    Board board{3, std::vector<player_type>(3, NONE)};
    int move = 0;

    void updateBoard(Board brd);

public:
    bool isValidMove(const Board &brd);
    bool isEnd();
    player_type nextPlayer();
    int getMove() const;
};

#endif //VISION_TTTBOARD_H
