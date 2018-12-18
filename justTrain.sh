[ -f MagicStuff/$1 ] && echo "Found" || cp $1 MagicStuff
cd MagicStuff


echo "Starting Steering Trainer"
sudo python3 LstmSteeringTrainer.py data.txt $2 &
echo "Starting Thrusting Trainer"
sudo python3 LstmThrustingTrainer.py data.txt $2 &
echo "Starting Shooting Trainer"
sudo python3 LstmShootingTrainer.py data.txt $2 
sudo python3 generatedMimic.py
