@echo off
echo WrongAnswers:  > wa.txt
FOR /L %%G IN (1,1,20) DO (
echo %%G.in > file.in

REM copy /y %%G.in XXX.in
REM copy /y %%G.in input.txt

python p3.py < file.in
REM python p3.py
REM python p3.py < file.in > %%G.out
REM python p3.py > %%G.out
REM python p3.py < %%G.in
REM python p3.py < %%G.in > %%G.out
REM python p3.py %%G.in > %%G.out
REM python p3.py %%G.in
REM python p3.py file.in

REM move XXX.out %%G.out
REM move file.out %%G.out
REM move output.txt %%G.out
REM move out.txt %%G.out
REM move output.out %%G.out

fc /w %%G.out %%G.ans || (pause && echo %%G >> wa.txt)
)
echo Congratulations!
PAUSE