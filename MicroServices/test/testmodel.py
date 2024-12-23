import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

model_path=r"D:\saved models\Ransomware\model_weights.pth"

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

model=CNNRNN3()
model.load_state_dict(torch.load(model_path)) 
model.eval()

image_path1 = r"D:\DATASETS\ransomware\CNN_dataset\Ransomware\RansomwareAleta_10.png"
image = Image.open(image_path1).convert("RGB")

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.RandomRotation(15),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])
input_tensor = transform(image).unsqueeze(0) 

with torch.no_grad():
    output = model(input_tensor)
    _, predicted_class = torch.max(output, 1)

print(f"Predicted class: {predicted_class.item()}")