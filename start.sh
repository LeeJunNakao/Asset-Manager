#!/bin/bash

if [ $PORT ]
then 
    uvicorn main:app --host 0.0.0.0 --port $PORT
else 
    uvicorn main:app --host 0.0.0.0 --port 80
fi