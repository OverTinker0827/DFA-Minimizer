# DFA Minimizer

This program performs **DFA minimization using the Myhill-Nerode table-filling method**.

---

## Features

- Reads a DFA from an input file.  
- Minimizes the DFA using the table-filling algorithm.  
- Writes the minimized DFA to an output file.  
- Optional visualization of the minimized DFA.

---

## Input Format

The input DFA file should follow the format shown in `input.txt`.

## Usage

Run the program using Python 3:

```bash
python3 main.py -i <input_file_location> -o <output_file_location> -v
```
- `-i` : Path to the input DFA file. **Default:** `input.txt`  
- `-o` : Path to save the minimized DFA. **Default:** `output.txt`  
- `-v` : Optional flag to visualize the minimized DFA
