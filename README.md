# ProjectCerebral

### This is our current project structure.

Vision scripts contain notebooks simply used for quick experimentation.

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


USE:
 1. Clone repo with `$ git clone ...`
 2. Activate conda enviroment with "$ conda activate"
 3. Open notebooks with "$ jupyter notebook"

