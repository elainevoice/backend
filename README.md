# Using the Backend of Elaine Voice

## Getting Started

These instructions will get you a copy up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
##### 1. Install the following software:
- [ ] [Python](https://www.python.org/)
- [ ] [PyTorch](https://pytorch.org/)
- [ ] (Optional for Linux GPU) [CUDA](https://developer.nvidia.com/cuda-downloads)
  * See the [Supported Graphic Cards](https://developer.nvidia.com/cuda-gpus)

### Installing
A step by step series of examples that tell you how to get a development environment running.

##### 1. (Optional) Activate VENV
You can activate VENV by using the following command: 
```console
python -m venv venv
```

##### 2. Installing the modules
After cloning the repository, navigate to the project folder and run the following command: 
```console   
python -m pip install -r requirements.txt
```

### Deployment
Once the containers have been installed, the project will be ready for deployment. 

##### 1. Start the Backend
Run the following command to start the backend
```console   
uvicorn main:app
```
or start it with watch/live-reload
```console   
uvicorn main:app --reload
```
