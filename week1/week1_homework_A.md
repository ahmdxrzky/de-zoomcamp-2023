# Answer for Homework Week 1 Part A

## Number 1
Execute code below to see help documentation for command _docker build_: <br>
```docker build --help``` <br>
Result: <br>
![number1](https://user-images.githubusercontent.com/99194827/214724884-9f6e5e99-a66e-4f54-bce8-631647372dd5.png)
From image above, it can be clearly seen that tag ```--iidfile string``` can be used for _Write the image ID to the file_. <br>

## Number 2
Execute code below to run docker based on python:3.9 image in interactive mode and entrypoint bash: <br>
```
docker run -it --entrypoint=bash python:3.9
```
Then, execute code below to check modules installed on the container: <br>
```
pip list
```
Result: <br>
![number2](https://user-images.githubusercontent.com/99194827/214727087-0cf22a1a-35d4-483a-8ede-729ae2d3fd56.png)
From image above, it can be clearly seen that there are already 3 modules being installed initially.

## Number 3
