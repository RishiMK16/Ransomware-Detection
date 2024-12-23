import socketio
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
import torch.nn as nn
import json

# Load the pre-trained model (same as your code)
class CNNRNN3(nn.Module):
    def __init__(self):
        super(CNNRNN3, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, 4, 2, 1),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 32, 4, 2, 1),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 64, 4, 2, 1),
            nn.BatchNorm2d(64)
        )
        self.lstm1 = nn.LSTM(64, 100, batch_first=True)
        self.dropout1 = nn.Dropout(0.1)
        self.lstm2 = nn.LSTM(100, 200, batch_first=True)
        self.fc1 = nn.Linear(200, 2)

    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1, 64)
        _, (h_n, _) = self.lstm1(x)
        x = self.dropout1(h_n[-1])
        _, (h_n, _) = self.lstm2(x.unsqueeze(1))
        x = self.fc1(h_n[-1])
        return x

model_path = r"D:\saved models\Ransomware\model_weights.pth"
model = CNNRNN3()
model.load_state_dict(torch.load(model_path))
model.eval()

# Transformation for incoming images
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.RandomRotation(15),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# Connect to the JavaScript Socket.IO server
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")
    sio.emit('AI_resp', "True")

@sio.event
def disconnect():
    print("Disconnected from the server.")

# Handle receiving image data and processing it
@sio.on('image_array')
def process_image(image_array):
    print("Received image array.")
    if not isinstance(image_array, dict):
        print("Error: image_array is not a dictionary")
        return

    payload = image_array.get('payload')
    if not payload:
        print("Error: 'payload' is missing or None")
        return sio.emit("AI_resp", "True")

    try:
        # Deserialize payload safely
        np_image = np.array(json.loads(payload), dtype=np.uint8)
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        print(f"Error processing payload: {e}")
        return

    # Convert the NumPy array into a PIL image
    try:
        image = Image.fromarray(np_image, mode='L')  # Convert to grayscale
    except ValueError as e:
        print(f"Error converting NumPy array to image: {e}")
        return

    # Apply transformations to the image
    input_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    # Perform the classification
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted_class = torch.max(output, 1)

    print(f"Predicted class: {predicted_class.item()}")

    # Send the predicted class back to the JavaScript server
    sio.emit('prediction', predicted_class.item())
    sio.emit("AI_resp", "True")

# Connect to the Socket.IO server at the specified URL
sio.connect('http://localhost:3334')

# Keep the connection alive to listen for incoming events
sio.wait()
