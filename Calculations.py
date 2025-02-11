from sensor_read import readSensor
import time
import numpy as np
import matplotlib.pyplot as plt

def calculate_com(sensor_values):
    """Calculate Center of Mass coordinates using 4 FSR sensor values."""
    F1, F2, F3, F4 = sensor_values
    W_door = 0                   # Weight of the door
    l_x = 0                      # Length along x-axis
    l_y = 0                      # Length along y-axis
    # Calculate x_com1
    x_com1 = l_x*((F1 + F2) - (W_door*0.5)) / (( (F1 + F2 + F3 +F4) - W_door) )

    # Calculate y_com1
    y_com1 = l_y*((W_door*0.5) -(F2 +F3)) / (-((F1 + F2 + F3 +F4)- W_door))

    return x_com1, y_com1

def plot_com(x, y, z):
    """Create/update 3D plot of force plate and CoM."""
    plt.ion()  # Enable interactive mode
    
    # Clear previous plot
    plt.clf()
    
    # Create 3D subplot
    ax = plt.axes(projection='3d')
    
    # Plot the force plate corners (assuming 30x30 cm plate)
    plate_corners = np.array([
        [-15, -15, 0],  # Sensor 1 Position
        [15, -15, 0],   # Sensor 2 Position
        [15, 15, 0],    # Sensor 3 Position
        [-15, 15, 0],   # Sensor 4 Position
    ])
    
    # Plot force plate
    ax.plot_trisurf(plate_corners[:,0], plate_corners[:,1], plate_corners[:,2], 
                    alpha=0.3, color='gray')
    
    # Plot sensors as points
    ax.scatter(plate_corners[:,0], plate_corners[:,1], plate_corners[:,2], 
              c='red', marker='o', s=100, label='Sensors')
    
    # Plot CoM
    ax.scatter(x, y, z, c='blue', marker='x', s=100, label='Center of Mass')
    
    # Set labels and title
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    ax.set_title('Force Plate CoM Visualization')
    # Set axis limits
    ax.set_xlim([-20, 20])
    ax.set_ylim([-20, 20])
    ax.set_zlim([0, 10])
    
    # Add legend
    ax.legend()
    
    # Update plot
    plt.draw()
    plt.pause(0.001)


if __name__ == "__main__":
        # Initialize plot
    plt.figure(figsize=(10, 8))
    
    # For Windows: 'COM3', 'COM4', etc.
    # For Linux: '/dev/ttyACM0', '/dev/ttyUSB0', etc.
    #sensor = readSensor(port='COM3', baudrate=115200)
    
    try:
        while True:
            # Read sensor values
            #values = sensor.Readsens()
            values = [10, 10, 10, 10]  # Dummy values for testing
            
            # Print all sensor values
            print(f"Sensor 1: {values[0]}")
            print(f"Sensor 2: {values[1]}")
            print(f"Sensor 3: {values[2]}")
            print(f"Sensor 4: {values[3]}")
            print("-" * 30)
            
            # Calculate and plot CoM
            
            x, y = calculate_com(values)
            input("Press Enter to calculate next CoM...")
            y,z = calculate_com(values)
            plot_com(x, y,z)
            
            time.sleep(0.1)  # Small delay to not flood the console
            
    except KeyboardInterrupt:
        print("\nStopping sensor reading...")
    #finally:
        #sensor.close()