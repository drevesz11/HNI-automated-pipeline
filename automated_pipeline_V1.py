import subprocess
import sys 

#Define which scripts will be called by the pipeline 
# Define the path to the environment.yml file
environment_yml = "/home/drevesz/Desktop/automated_pipeline/HNI-automatedpipeline/environment.yml"


#Define working directory from which the scripts are derived 
working_directory = "/home/drevesz/Desktop/automated_pipeline/HNI-automatedpipeline"


#Call the scripts sequentially 
#    subprocess.run(["python", script_path], check=True)


#Step 1 ensure Anaconda 2.3.1 installed for setting up the virtual environment 
try:
    # Run 'anaconda-navigator --version' to get the version
    result = subprocess.run(["anaconda-navigator", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout.strip()
    
    # Check if the output contains the version and if it's at least 2.3.1
    if "2.3.1" not in output:
        print("Anaconda Navigator version 2.3.1 or higher is required. Installing Anaconda Navigator...")
        # Install Anaconda Navigator using 'conda'
        subprocess.run(["conda", "install", "anaconda-navigator"], check=True)
    else:
        print("Anaconda Navigator version 2.3.1 or higher is already installed.")
except FileNotFoundError:
    print("Anaconda Navigator is not found. Installing Anaconda Navigator...")
    # Install Anaconda Navigator using 'conda'
    subprocess.run(["conda", "install", "anaconda-navigator"], check=True)



#Step 2 --> Create a virtual environment and install dependencies
try:
    # Create a new conda environment named 'myenv' and install the dependencies
    subprocess.run(["conda", "env", "create", "--file", environment_yml], check=True)
    
    # Activate the created virtual environment
    subprocess.run(["conda", "activate", "myenv"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error creating or activating the conda environment: {e}")


# Now, you can continue with the rest of your script, and the virtual environment is active.