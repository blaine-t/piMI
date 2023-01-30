#!/bin/bash

x=0

while IFS='$\n' read -r line; do
    input=$line

    if $(echo "$input" | grep -q 'c'); then
        continue
    fi

    cleanInput=$(echo $input | tr '|│' ' ' | sed 's/  */ /g')   # Clean up
    length=$(echo $cleanInput | grep -o ' ' | wc -l)            # Get the number of fields for the loop

    echo -n [   # Start the square brackets

    for i in $( seq 1 $length); do
        currentValue=$(echo $cleanInput | cut -d ' ' -f $i )

        # Convert byte letters to numbers using sed
        cleanValue=$(echo $currentValue | sed -r 's/[bB]+/''/g' | sed -r 's/[kK]+/000/g' | sed -r 's/[mM]+/000000/g' | sed -r 's/[gG]+/000000000/g' | sed -r 's/[tT]+/000000000000/g')

        echo -n "$cleanValue"

        if [ $i -lt $length ]; then
            echo -n ","
        fi
    done
    echo ]      # Finish the square brackets and end
done
