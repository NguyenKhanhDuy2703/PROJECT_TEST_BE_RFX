set shell := ["powershell.exe", "-c"]

build :
    @echo "Building the project..."
    # Add your build commands here
    pip install -r requirements.txt