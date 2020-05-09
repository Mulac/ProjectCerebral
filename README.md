# ProjectCerebral

### This is our current project structure.

Boards is a package that contains all the logic we need for each board game.

There are then 3 main components: **Vision**, **AI** and **Control**.
The vision finds lines and circles which are then sent to the board classes to compute valid states.
The AI module uses a negamax algorithm with alpha beta pruning for efficiency.
Control is designed specifically for our robot to compute the joint parameters and send these to our motor controller on the Lego EV3.

There is also **helper.py** containing useful classes such as Position and Player used by all modules.

ProjectCerebral<br>
├── robot<br>
│    ├── __init__.py<br>
|    ├── boards<br>
|    │    ├── __init__.py<br>
|    │    ├── board.py<br>
|    │    ├── nmmBoard.py<br>
|    │    └── tttBoard.py<br>
|    |
|    ├── vision.md<br>
|    ├── negamax.py<br>
|    ├── control.py<br>
|    └── helper.py<br>
|
└── main.py<br>


## USE
 1. Clone repo with `$ git clone https://github.com/Mulac/ProjectCerebral.git`
 2. Install anaconda https://www.anaconda.com/distribution/ - we use conda enviroments to manage dependancies
 3. `cd` into ProjectCerebral directory
 4. `conda env create -f environment.yml` to create enviroment from yaml file
 5. `conda activate robot` to enter the enviroment
 6. `python main.py` to run the main loop

