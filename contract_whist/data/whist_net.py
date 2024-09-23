import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

from contract_whist.players import DataPlayer
from contract_whist.data.data_gen import HarvestData

# Create a dataset (X_train: game states, y_train: correct cards to play)
# X_train: shape [num_samples, input_size]
# y_train: shape [num_samples] (indices of the correct card to play, not one-hot encoded)

players = [
    DataPlayer(name, 1.05, 0.35, 6)
    for name in ("Fred", "Murray", "Sam", "Tim")
]
X_train, y_train = HarvestData(players).get_data(hands=[7, 7, 7, 7, 7],
                                                 num_games=1000)

# Create a DataLoader to handle batching
train_dataset = TensorDataset(torch.from_numpy(X_train.astype(np.float32)),
                              torch.from_numpy(y_train.astype(np.float32)))
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
_, input_size = X_train.shape  # Size of the input vector (game state encoding)
hidden_size = 128  # Number of neurons in the hidden layers
_, output_size = y_train.shape   # Number of possible cards to play (or bids, etc.)

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
