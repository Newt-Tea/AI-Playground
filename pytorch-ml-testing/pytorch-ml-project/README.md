# PyTorch Machine Learning Project

This project utilizes the MNIST database to explore various machine learning techniques using PyTorch. The goal is to develop and evaluate models for digit recognition and classification.

## Project Structure

```
pytorch-ml-project
├── data
│   └── niss_fingerprint_database
├── notebooks
│   └── exploration.ipynb
├── src
│   ├── data_preprocessing.py
│   ├── model.py
│   └── train.py
├── requirements.txt
└── README.md
```

- **data/niss_fingerprint_database**: Contains the NISS fingerprint database for training and testing.
- **notebooks/exploration.ipynb**: Jupyter notebook for exploratory data analysis and experimentation.
- **src/data_preprocessing.py**: Functions for loading and preprocessing the fingerprint data.
- **src/model.py**: Defines the machine learning model architecture using PyTorch.
- **src/train.py**: Contains the training loop for the model, including validation and saving weights.

## Setup Instructions

### Get the code

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pytorch-ml-project
   ```

2. Download the MNIST database and place it in the `data/niss_fingerprint_database` directory.

### Set up the Container

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pytorch-ml-project
   ```

2. Build the Docker image:
   ```
   docker build -t pytorch-ml-project .
   ```

3. Run the Docker container:
   ```
   docker run -p 8888:8888 -v $(pwd):/app pytorch-ml-project
   ```

   This command maps port 8888 on your host to port 8888 in the container and mounts the current directory to `/app` in the container.

4. Access Jupyter Notebook:
   Open your web browser and go to `http://localhost:8888`. You should see the Jupyter Notebook interface.

## Usage

- Use the `exploration.ipynb` notebook for initial data exploration and visualization.
- Modify the `data_preprocessing.py` file to customize data loading and preprocessing steps.
- Define your model architecture in `model.py` and implement the training logic in `train.py`.
- Run the training script to train your model on the NISS fingerprint data.

## Objectives

- Experiment with different machine learning techniques for fingerprint recognition.
- Evaluate model performance and explore potential improvements.
- Document findings and results in the Jupyter notebook.