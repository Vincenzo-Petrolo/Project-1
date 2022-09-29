# Project 1 main

from programs import program1,program2,program3
import os

def main():  
  #menu description
  menu =  "############  MENU ##############\n"+\
          "[1] Single TV - Single Fault\n"+\
          "[2] Single TV - All Faults\n"+\
          "[3] Fault coverage of 1-10 TVs\n"+\
          "############  MENU ##############\n"
  
  choice = 0
  
  # Show the menu
  while (choice not in [1,2,3]):
    os.system("clear")
    print(menu)
    choice = int(input("Write the number of the program you want to execute: "))
    
  # Once the user makes a choice, run the specific program
  if (choice == 1):
    program1()
    return
  elif (choice == 2):
    program2()
    return
  elif (choice == 3):
    program3()
    return
  else:
    print("Error on the choice, returning")
    return


if __name__ == "__main__":
  main()

