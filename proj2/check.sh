#!/bin/bash
rm p3
rm *.out
rm *.txt
rm -rf class
#rm p3.cpp
#mv *.cpp p3.cpp

#gcc -o p3 p3.c -lm
#g++ -std=c++14 -o p3 p3.cpp
#javac -d class *.java

echo "WrongAnswers:"  > wa.txt
echo "AcceptedAnswers:"  > ac.txt
for i in {1..20}
do
	#echo "$i.in" > file.in
	#echo "$i" > file.in
	printf "$i.in\n$i.out" > file.in
	
	
	#cp $i.in input.txt
	
	#java -cp class Q3
	#java -cp class Main
	#java -cp class Main < file.in
	#java -cp class Main < $i.in
	#java -cp class Main < file.in > $i.out
	#java -cp class Main < $i.in > $i.out
	
	#./p3 < file.in
	#./p3 $i.in $i.out
	#./p3 < $i.in > $i.out
	#./p3

	python3 p3.py < file.in
	#python p3.py < file.in
	
	
	#mv output.txt $i.out
	#mv Chord.out $i.out
	
	
	if diff --strip-trailing-cr -E $i.out $i.ans; then
		echo "$i" >> ac.txt
		printf "$i correct\n"
	else
		echo "$i" >> wa.txt
	fi
done
