#!/bin/bash

echo "Hey Yo, I heard you like wrappers so I wrapper your wrapper in a wrapper"
#!/bin/bash
# Basic range in for loop

echo "$3"
./autoScript.sh $1 $2 -nd -nd
val="$3"+1
for (( i=0; i <= $val; i++ )) 
do          
        
        ./autoScript.sh $1 $2 -od -nw -c
done
echo All done
