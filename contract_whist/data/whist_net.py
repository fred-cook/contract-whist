import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Create a dataset (X_train: game states, y_train: correct cards to play)
# X_train: shape [num_samples, input_size]
# y_train: shape [num_samples] (indices of the correct card to play, not one-hot encoded)
X_train = torch.rand(1000, 163)  # Example random data, replace with your real game state data
y_train = torch.randint(0, 52, (1000,))  # Example random target data, replace with your labels

# Create a DataLoader to handle batching
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Define the neural network
class WhistNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(WhistNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)  # Output logits, don't apply softmax here (it's applied in the loss function)
        return x

# Hyperparameters
input_size = 163  # Size of the input vector (game state encoding)
hidden_size = 128  # Number of neurons in the hidden layers
output_size = 52   # Number of possible cards to play (or bids, etc.)

# Initialize the model, loss function, and optimizer
model = WhistNet(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()  # Loss function for classification
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer

# Training loop
num_epochs = 10  # Set the number of epochs
for epoch in range(num_epochs):
    total_loss = 0.0
    for game_state, correct_action in train_loader:
        # Forward pass
        outputs = model(game_state)
        
        # Compute the loss
        loss = criterion(outputs, correct_action)  # correct_action is the index of the correct card
        
        # Backward pass and optimization
        optimizer.zero_grad()  # Clear the previous gradients
        loss.backward()  # Backpropagation
        optimizer.step()  # Update weights

        total_loss += loss.item()
    
    # Print average loss for this epoch
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss/len(train_loader):.4f}')

# Save the model after training
torch.save(model.state_dict(), 'whist_model.pth')
