#!/bin/bash

OD="FALSE"
NT="FALSE"
NW="FALSE"
LSTM="TRUE"
DATASIZE="1000"
C="FALSE"
for arg in "$@"
do
    if [[ "$arg" == "--oldData" ]] || [[ "$arg" == "-od" ]]
    then
        echo "Training will use old data"
        OD="TRUE"
    fi
    if [[ $arg == "--bigData" ]] || [[ $arg == "-bd" ]]
    then
        echo "100,000 pieces of training data will be generated"
        echo "It's BIIIIGGGGG DATAAAAAA"
        DATASIZE="100000"
    fi
    if [[ $arg == "--newData" ]] || [[ $arg == "-nd" ]]
    then
        echo "Training Data will be reset"
        echo "Goodbye old data!"
        > MagicStuff/data.txt
    fi
    if [[ $arg == "--feedForward" ]] || [[ $arg == "-ff" ]]
    then
        echo "Training will use a Feed Forward Network instead of LSTM"
        LSTM="FALSE"
    fi
    if [[ "$arg" == "--noTrain" ]] || [[ "$arg" == "-nt" ]]
    then
        echo "Script will only generate data"
        NT="TRUE"
    fi
    if [[ "$arg" == "--noWait" ]] || [[ "$arg" == "-nw" ]]
    then
        echo "Script will not wait for user to finish"
        NW="TRUE"
    fi
    if [[ "$arg" == "--continue" ]] || [[ "$arg" == "-c" ]]
    then
        echo "Script will continue training from previous trained network"
        C="TRUE"
    fi
done


sudo /bin/cp -rf $1 MagicStuff
cd MagicStuff
sudo python3 xpilotDataMinerConfigurable.py $1 $DATASIZE


./xpilots -noQuit 1 -switchBase  1 -map maps/lifeless.xp -fps 40 -robots 3 >/dev/null &






if [[ "$OD" != "TRUE" ]]
then
        sudo python3 dataGenBot.py
fi
if [[ "$LSTM" == "TRUE" ]] && [[ "$NT" == "FALSE" ]];
then
        echo "Starting Steering Trainer"
        sudo python3 LstmSteeringTrainer.py data.txt $2 $C &
        p1=$!
        echo "Starting Thrusting Trainer"
        sudo python3 LstmThrustingTrainer.py data.txt $2 $C &
        p2=$!
        echo "Starting Shooting Trainer" 
        sudo python3 LstmShootingTrainer.py data.txt $2 $C &
        p3=$!
        
        stop="no"
        if [[ "$NW" == "FALSE" ]]
        then      
                echo "To cancel the script type 'stop' and hit enter"
                read stop
        fi
        if [[ "$stop" == "stop" ]]
        then
            sudo kill $p1
            sudo kill $p2
            sudo kill $p3    
        else
            wait $p1
            wait $p2
            wait $p3
            if [[ "$NW" == "FALSE" ]]
            then
                echo "Press Enter to Start Mimic"
                read key
            fi
            sudo python3 generatedMimic.py
        fi
fi
if [[ "$LSTM" == "FALSE" ]] && [[ "$NT"=="FALSE" ]]
then
        echo "Starting Steering Trainer"
        sudo python3 ffSteeringTrainer.py data.txt $2 $C &
        p1=$!
        echo "Starting Thrusting Trainer"
        sudo python3 ffThrustingTrainer.py data.txt $2 $C &
        p2=$!
        echo "Starting Shooting Trainer" 
  
        sudo python3 ffShootingTrainer.py data.txt $2 $C &
        p3=$!
        stop="no"
        if [[ "$NW" == "FALSE" ]]
        then        
                echo "To cancel the script type 'stop' and hit enter"
                read stop
        fi
        if [[ "$stop" == "stop" ]]
        then
            sudo kill $p1
            sudo kill $p2
            sudo kill $p3    
        else
            wait $p1
            wait $p2
            wait $p3
            if [[ "$NW" == "FALSE" ]]
            then
                echo "Press Enter to Start Mimic"
                read key
            fi
            sudo python3 generatedMimic.py
        fi
fi
