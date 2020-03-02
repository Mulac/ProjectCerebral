# ProjectCerebral

### This is our current project structure.

vision_scripts contain notebooks simply used for quick experimentation.

ProjectCerebral<br>
├── boards<br>
│   ├── __init__.py<br>
│   ├── board.py<br>
│   ├── nmmBoard.py<br>
│   └── tttBoard.py<br>
├── main.py<br>
├── README.md<br>
└── vision.py<br>

We will have 3 main components: vision, ai and control.
Boards is a package that contains all the logic we need for each board game.
AI will be a package that contains a agent for each game.
Vision is a module that contains all the generic vision functions.
Control will be a module that contains an interface for communicating with the ev3.


## USE
 1. Clone repo with `$ git clone https://github.com/Mulac/ProjectCerebral.git`
 2. Install anaconda https://www.anaconda.com/distribution/ - we use conda enviroments to manage dependancies
 3. `cd` into ProjectCerebral directory
 4. `conda env create -f environment.yml` to create enviroment from yaml file
 5. `conda activate robot` to enter the enviroment
 6. `python main.py` to run the program

