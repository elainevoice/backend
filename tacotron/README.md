# Using Docker Compose with Docker Compose

## Getting Started

These instructions will get you a copy up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
##### 1. Install the following software:
- [ ] [Docker](https://www.docker.com/)

### Installing
A step by step series of examples that tell you how to get a development environment running.

##### 1. Build the Docker Containers
Run the following command to start the docker container
```console   
docker-compose build
```

### Deployment
Once the containers have been installed, the project will be ready for deployment. 

##### 1. Start the Docker Containers
Run the following command to start the containers
```console   
docker-compose up
```

### Development
Here are some useful tools to help you while developing!

##### Finding the name of a container
Run the following command to find containers
```console   
docker container ls
```

##### Entering the docker container
After that use the following command to enter the container
```console   
docker exec -it <CONTAINER_NAME> /bin/sh
```

##### Installing a new package
Enter the docker container.
```console
npm install <package>
```

### Preparing a Dataset
Each dataset requires a .csv file separated by pipes '|'.
The CSV file of metadata requires the following parameters:
* **ID**: this is the name of the corresponding .wav file
* **Transcription**: words spoken by the reader (UTF-8)
* **Normalized Transcription**: transcription with numbers, ordinals, and monetary units expanded into full words (UTF-8).

### Training a Model
Make sure your containers are succesfully deployed.

##### 1. Enter your Docker Container
Execute the following command to enter your docker container
```console   
docker exec -it <CONTAINER_NAME> /bin/sh
```

##### 2. Preprocess the model
Execute the following command within your docker container to train the model
```console   
python preprocess.py --path <PATH>
```

##### 3. Train the model
Execute the following command within your docker container to train the model
```console   
python train_tacotron.py
```