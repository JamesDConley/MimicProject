# MimicProject
Using Machine Learning to automatically generate Agents that mimic hard-coded python bots

In order to use the system
-Make sure you have PyBrain installed for Python 3.  Also requires SciPy and NumPy
-Have an Xpilot Python Bot ready to Mimic (Or use the one included, smarto.py)
From Here You Have Two Options
  1 - Iterative Learning (Generally works better)
      This system creates a poor mimic and then iteratively runs and retrains based on comparisons with the original bots actions
      
      Syntax is ./iterativeLearning.sh [somePythonBot.py] [Epochs Per Iterations (an int)] [Number of Iterations (int)]
      
  2 - Regular Training (Lots of options but generally not as effective)
  
      For this I really suggest looking at the .sh file itself because there are many options but in general
      ./autoSystem.sh [somePythonBot.py] [Epochs to train for] [extra options]
      extra options that can be useful include:
        -nd (new data, deletes the old data)
        -od (Old Data, doesn't generate any new data)
        -bd (Big Data, generates a large dataset for training)
        -ff (Trains Feed Forward Networks Instead of LSTM)
        -nt (No Training, Generates Data but doesn't train anything)
        -nw (No wait, the script will not wait for the user to finish)
        -c (continue, the script will load previously trained models and train them further rather than creating new ones)
 
 In order to select different inputs for the machine learning models alter the config.txt in the magicstuff folder.  You'll notice there are different methods for adding information to seperate networks (Steering, Thrusting, Shooting) and a single method to add a variable to all of these.  Inputs should be in the form of a float, and ideally they should be normalized for the range (-1, 1) but it is not entirely necessary to do so.
 
 The Mimic that is output will also generate training data on itself based on what the original bot would do in the situations it steers itself into
 
