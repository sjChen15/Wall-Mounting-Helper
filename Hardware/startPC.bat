@echo off

echo Starting Img Receive Function
start "" py image_receive_process_pc.py 

echo Starting Main PC
start "" py mainPC.py 