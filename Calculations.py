from sensor_read import readSensor
import time
import numpy as np
import matplotlib.pyplot as plt

# def average_sensor_values(sensor, duration=5):
#      """Reads sensor values for a specified duration and returns their average."""
#      values_list = []
#      start_time = time.time()
    
#      while time.time() - start_time < duration:
#          values = sensor.Readsens()  # Read sensor values
#          values_list.append(values)
#          time.sleep(0.1)  # Small delay to prevent overloading the sensor
        
#      # Convert the list to a numpy array and calculate the mean along the rows (axis=0)
#      values_array = np.array(values_list)
#      averaged_values = np.mean(values_array, axis=0)
    
#      return averaged_values

def calculate_com(sensor_values):
    """Calculate Center of Mass coordinates using 4 FSR sensor values."""
    F1, F2, F3, F4 = sensor_values
    #print(f" F1= {F1}, F2={F2},  F3={F3}, F4={F4}")
    #F1= F1-44.58
    #F2= F2-28.78
    #F3 = F3-49.28
    #F4= F4-47.98
    #F4, F3, F2, F1 = sensor_values
    W_door = 17*9.81                   # Weight of the door
    l_x = 2.026 +0.06                      # Length along x-axis
    l_y = 0.861 +0.06                   # Length along y-axis
    # Calculate x_com1
    x_com1 = l_x*((F1 + F2) - (W_door*0.5)) / (( (F1 + F2 + F3 +F4) - W_door) )
    #x_com= ((F1*l_x+F2*l_x+F3*0+F4*0)-)
    # Calculate y_com1
    y_com1 = l_y*((W_door*0.5) -(F2 +F3)) / (-((F1 + F2 + F3 +F4)- W_door))

    #print(f"XCOM= {x_com1}, YCOM={y_com1}")

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
        [2.0, 0, 0],  # Sensor 1 Position
        [2.0, 0.85, 0],   # Sensor 2 Position
        [0, 0.85, 0],    # Sensor 3 Position
        [0, 0, 0],   # Sensor 4 Position
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
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Force Plate CoM Visualization')
    # Set axis limits
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([0, 3])
    
    # Add legend
    ax.legend()
    
    # Update plot
    plt.draw()
    plt.pause(0.001)



if __name__ == "__main__":
        # Initialize plot
    plt.figure(figsize=(6, 4))
    
    # For Windows: 'COM3', 'COM4', etc.
    # For Linux: '/dev/ttyACM0', '/dev/ttyUSB0', etc.
    sensor = readSensor(port='COM7', baudrate=115200)
    
    try:
        while True:
            # Read sensor values
            values = sensor.Readsens()  # Read sensor values
            #values = average_sensor_values(sensor, duration=5)
                    
            # Print all sensor values
            print(f"F 1: {values[0]}")
            print(f"F 2: {values[1]}")
            print(f"F 3: {values[2]}")
            print(f"F 4: {values[3]}")
            print("-" * 30)
            print(values[0]+values[1]+values[2]+values[3])
            
            # Calculate and plot CoM
            # z,j = calculate_com(values)
            # print()
            

            # x, y = calculate_com(values)
            # input("Press Enter to calculate next CoM...")
            # x, y = calculate_com(values)
            # #z,y = calculate_com(values)
            

            choice=input("Enter the calculation 1) Print XY ____ 2) Print Z ____  3) Print ALL values")
            match choice:
                case "1":
                    print("**********************")
                    values = sensor.Readsens()  # Read sensor values
                    x=0
                    y=0
                    x, y = calculate_com(values)
                    x=x-0.08
                    y=y-0.08
                    print(f"X= {x} -- Y= {y}") 
                    print("**********************")
                    #sensor.close()
                case "2":
                    print("**********************")
                    values = sensor.Readsens()  # Read sensor values
                    z=0
                    j=0
                    z,j = calculate_com(values)
                    print(f"Z=  {z}      Y= {j} ")
                    print("**********************")
                case "3":
                    print("**********************")
                    sensor = readSensor(port='COM7', baudrate=115200)
                    time.sleep(0.1) 
                    values = sensor.Readsens()  # Read sensor values
                    z=0
                    j=0
                    x=0
                    y=0
                    z,j = calculate_com(values)
                    sensor.close
                    input("Press Enter to calculate next CoM...")
                    sensor = readSensor(port='COM7', baudrate=115200)
                    time.sleep(0.1) 
                    values = sensor.Readsens()  # Read sensor values
                    x, y = calculate_com(values)
                    print("**********************")
                    #x= x-0.23
                    plot_com(x, y, z)
                    print()
                    print(f"X= {x}     Y= {y}     Z= {z}")
                    print("**********************")
                    sensor.close()
                    #time.sleep(0.1)  # Small delay to not flood the console
                    #sensor.close()
            
    except KeyboardInterrupt:
        print("\nStopping sensor reading...")
    #finally:
        sensor.close()