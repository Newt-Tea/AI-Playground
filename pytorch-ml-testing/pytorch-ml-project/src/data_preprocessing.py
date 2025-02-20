import os
from sklearn.model_selection import train_test_split
from torchvision import transforms
from PIL import Image

def load_data(data_dir):
    """
    Load images and labels from the MNIST dataset directory.

    Args:
        data_dir (str): Path to the MNIST dataset directory.

    Returns:
        images (list): List of image file paths.
        labels (list): List of corresponding labels.
    """
    images = []
    labels = []
    
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)
        if os.path.isdir(label_dir):
            for img_file in os.listdir(label_dir):
                img_path = os.path.join(label_dir, img_file)
                images.append(img_path)
                labels.append(label)
    
    return images, labels

def preprocess_images(images):
    """
    Preprocess images by resizing and converting to tensor.

    Args:
        images (list): List of image file paths.

    Returns:
        processed_images (list): List of processed image tensors.
    """
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])
    
    processed_images = []
    for img_path in images:
        image = Image.open(img_path).convert('RGB')
        image = transform(image)
        processed_images.append(image)
    
    return processed_images

def split_data(images, labels, test_size=0.2, random_state=42):
    """
    Split the data into training and testing sets.

    Args:
        images (list): List of processed image tensors.
        labels (list): List of corresponding labels.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        train_images (list): Training images.
        test_images (list): Testing images.
        train_labels (list): Training labels.
        test_labels (list): Testing labels.
    """
    return train_test_split(images, labels, test_size=test_size, random_state=random_state)

def main(data_dir):
    """
    Main function to load, preprocess, and split the MNIST dataset.

    Args:
        data_dir (str): Path to the MNIST dataset directory.

    Returns:
        train_images (list): Training images.
        test_images (list): Testing images.
        train_labels (list): Training labels.
        test_labels (list): Testing labels.
    """
    images, labels = load_data(data_dir)
    processed_images = preprocess_images(images)
    train_images, test_images, train_labels, test_labels = split_data(processed_images, labels)
    
    return train_images, test_images, train_labels, test_labels

if __name__ == "__main__":
    data_directory = '../data/mnist'
    train_images, test_images, train_labels, test_labels = main(data_directory)