import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from src.data_preprocessing import load_data, preprocess_data
from src.model import MyModel

def train_model(model, train_loader, criterion, optimizer, num_epochs):
    model.train()
    for epoch in range(num_epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

def main():
    # Load and preprocess data
    train_data, train_labels = load_data('data/niss_fingerprint_database')
    train_data = preprocess_data(train_data)

    # Create DataLoader
    train_loader = DataLoader(list(zip(train_data, train_labels)), batch_size=32, shuffle=True)

    # Initialize model, criterion, and optimizer
    model = MyModel()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Train the model
    train_model(model, train_loader, criterion, optimizer, num_epochs=10)

    # Save the trained model
    torch.save(model.state_dict(), 'model_weights.pth')

if __name__ == '__main__':
    main()