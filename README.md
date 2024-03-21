# README

# **Python Simulation of Antigen Spread and Response**

## **Overview**

This project simulates the spread and response of antigens within a given landscape. It includes the following main components: `Main.py`, `Antigen.py`, `Landscape.py`, and `Storage.py`. The simulation models antigens on a grid, visualizes their spread, and tracks changes over time.

## **Files Description**

### **`Main.py`**

- **Purpose**: Acts as the entry point for the simulation.
- **Functionality**: Initializes a landscape, randomly generates antigens, and runs the simulation for a set period, outputting the state of the landscape and antigens at various points.

### **`Antigen.py`**

- **Purpose**: Defines the Antigen class.
- **Functionality**: Handles the properties of an antigen such as spread, memory, and response. Includes methods for getting and setting these properties, and calculates baseline response based on certain parameters.

### **`Landscape.py`**

- **Purpose**: Defines the Landscape class.
- **Functionality**: Manages the simulation landscape. Maintains a grid of antigens, updates their states, handles the addition of new antigens, and visualizes the landscape using a 3D plot. Includes methods for time progression, antigen interaction, and landscape analysis.

### **`Storage.py`**

- **Purpose**: Provides a simple Storage class.
- **Functionality**: Used for storing snapshots of the landscape at different time points. Holds data and time attributes.

## **Running the Simulation**

To run the simulation, simply execute the `Main.py` script. This will initialize the landscape and antigens and run the simulation for a predetermined number of cycles. Outputs include printed states of the landscape and a graphical representation.

## **Dependencies**

- NumPy: Used for numerical operations.
- Matplotlib: Required for plotting the landscape in 3D.

Ensure these dependencies are installed before running the simulation.