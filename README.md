# adalm-stimulation

## Description
This repository contains code to interface with the Analog Devices ADALM1000. The code allows for voltage or current-controlled stimulation and automatically records current and voltage. 

## Prerequisites
- Windows operating system
- Git (for cloning the repository)
- Administrator access to install dependencies

## Windows Installation Instructions

1. Clone the repository:
```powershell
git clone https://github.com/WinnemacLabs/adalm-stimulation.git
cd adalm-stimulation
```

2. Install libsmu c++ dependencies:
   - Download from: https://github.com/analogdevicesinc/libsmu/releases/tag/v1.0.4
   - [Add specific instructions about which file to download and how to install it]

3. Install pyenv-windows from PowerShell (run as administrator):
```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

4. Close and reopen PowerShell

5. Install Python 3.10:
```powershell
pyenv install 3.10.11
```

6. Create a new virtual environment with Python 3.10:
```powershell
# Navigate to your project directory (skip if you're already there)
cd adalm-stimulation

# Create new venv with Python 3.10
pyenv local 3.10.11
python -m venv venv-py310
```

7. Activate the virtual environment:
```powershell
.\venv-py310\Scripts\activate
```

8. Install required Python packages:
```powershell
pip install -r requirements.txt
```

## Mac Installation Instructions

1. Clone the repository:
```powershell
git clone https://github.com/WinnemacLabs/adalm-stimulation.git
cd adalm-stimulation
```


## Usage
Programs should be run while ADALM1000 is plugged into USB port. 


## Troubleshooting
Common issues and their solutions:
- [Add common installation or runtime issues users might encounter]
- [Add solutions to these issues]

## License
[Add license information]

## Contact
Rachel Daso (racheldaso2027@u.northwestern.edu)

Alexander Curtiss (alexander.curtiss@winnemaclabs.com)
