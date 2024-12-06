# QM_GUI

This Python project implements the Quine-McCluskey algorithm, a method for simplifying Boolean functions. It includes a user-friendly GUI to input minterms and don't-care terms, calculate minimized expressions in Sum-of-Products (SOP) form, and convert them to Product-of-Sums (POS) form.

## Features

- **Minimize Boolean Functions**: Efficiently simplifies expressions using the Quine-McCluskey algorithm.
- **SOP to POS Conversion**: Converts minimized expressions from SOP to POS form.
- **Graphical User Interface (GUI)**: Intuitive GUI built with Tkinter for user interaction.
- **File Handling**: Supports loading minterms and don't-care terms from files and saving output results.
- **Execution Time Tracking**: Displays the time taken to perform the minimization.
- **Clear and Save Options**: Easily clear inputs or save results to a file.

1. Enter the **minterms** and **don't-care terms** as comma-separated values in the input fields.

2. Click on:
   - **Calculate**: To minimize the Boolean function.
   - **Convert to POS**: To convert the SOP expression into POS form.
   - **Clear**: To reset all inputs and outputs.
   - **Load File**: To load minterms and don't-care terms from a text file.
   - **Save Output**: To save the result to a file.

3. The minimized expression and execution details will be displayed in the output box.

## Input and Output Format (for GUI)
- **Input**:
  - Minterms: 2,3,7,9,11,13
  - Don't-care terms: 1,10,15

  - **Output**:
    Minimized Expression (SOP):
    B'C + AD + CD
    Number of Product Terms: 3
    Execution Time: 0.000213 seconds

## Input and Output Format (to load a .txt file)
  - Open notepad
  - In the first line, write all your minterms
  - In the second line, write your don't cares (if there are no don't cares, simply press enter after minterms and leave it blank)
  - Save as .txt and then load file using button in GUI




