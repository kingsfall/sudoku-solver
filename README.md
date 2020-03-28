# Sudoku Solver

As the name suggests, this is a script that helps to solve a 9x9 Sudoku puzzle. It is built on python.

Simply put, I am using a rule-based method for solving the puzzle. The rules programmed into this solver are based on the intrinsic rules of the game. Which is pretty straight forward...

```
Rule: Each row, column, and nonet can only contain a unique number (1 to 9) exactly once. No duplicates allowed
```
![Image of sudoku rules](http://www.dragonsudoku.co.uk/sudoku-grid-1.gif)

A human player would identify a list of possible numbers for every cell in the 9x9 puzzle. The list of numbers will be created based on elimination method by referencing the cell's column, row and nonet. Going through the code, you will identify pieces of functions that codifies this human solving method into computer automation.

# Brief description of functions

## Step 1:
```
def find_possible_numbers(row,pointer_y,pointer_x,container,possible_num,possible_num_list):
    for pointer_y in range(row):
        for pointer_x in range(len(container[pointer_x])):
            if (container[pointer_y][pointer_x] != 0 and type(container[pointer_y][pointer_x]) != list):
                possible_num.remove(container[pointer_y][pointer_x])
        possible_num_list.append(possible_num)
        possible_num = [1,2,3,4,5,6,7,8,9]

    return possible_num_list
	
def find_possible_numbers_box(row,pointer_y,pointer_x,container,possible_num,possible_num_list):
    total_box = 9
    base_y = 0
    total_y = 0
    base_x = 0
    total_x = 0
    for num_box in range(1,total_box+1):
        
        for pointer_y in range(3):
            total_y = base_y + pointer_y
            for pointer_x in range(3):
                total_x = base_x + pointer_x
                if container[total_y][total_x] != 0 and type(container[pointer_y][pointer_x]) != list:
                    possible_num.remove(container[total_y][total_x])
        possible_num_list.append(possible_num)
        possible_num = [1,2,3,4,5,6,7,8,9]

        base_x = base_x + 3
        if (num_box%3) == 0:
            base_y = base_y + 3
            base_x = 0
        ++num_box
    
               
    return possible_num_list

	
```

This functions will loop through all the cells in either a row, column or nonet and returns an array possible of numbers based on elimination.

```
def check_for_overlaps(possible_num_list_horizontal,possible_num_list_vertical,possible_num_list_box,container,appendlist):
    total_box = 9
    base_y = 0
    total_y = 0
    base_x = 0
    total_x = 0
    appendedcontainernumbers = 0
    for num_box in range(1,total_box+1):
        for pointer_y in range(3):
            total_y = base_y + pointer_y
            for pointer_x in range(3):
                total_x = base_x + pointer_x
                if container[total_y][total_x] == 0:
                    overlap = set(possible_num_list_horizontal[total_y]) & set(possible_num_list_vertical[total_x]) & set(possible_num_list_box[num_box-1])
                    overlap = list(overlap)
                    if len(overlap) == 1:
                        container[total_y][total_x] = overlap[0]
                        appendedcontainernumbers +=1
                    elif appendlist == 1:
                        container[total_y][total_x] = overlap
        base_x = base_x + 3
        if (num_box%3) == 0:
            base_y = base_y + 3
            base_x = 0
        ++num_box
    appendedContainer = container
    
    return appendedContainer,appendedcontainernumbers
```

For every cell, find_possible_numbers function will run thrice to return 3 array of possible numbers. This function (check_for_overlaps) will check for overlaping numbers between the 3 arrays of possible numbers created after referencing rows, columns and nonets. This will further eliminate numbers that are not overlapped. 

```
def loop_process(container,appendlist):
    possible_num_list_horizontal = find_possible_numbers(row,pointer_y,pointer_x,container,[1,2,3,4,5,6,7,8,9],[])
    t_container = list(map(list, zip(*container)))
    possible_num_list_vertical = find_possible_numbers(row,pointer_y,pointer_x,t_container,[1,2,3,4,5,6,7,8,9],[])
    possible_num_list_box = find_possible_numbers_box(row,pointer_y,pointer_x,container,[1,2,3,4,5,6,7,8,9],[])
    appendedContainer, appendedcontainernumbers = check_for_overlaps(possible_num_list_horizontal,possible_num_list_vertical,possible_num_list_box,container,appendlist)
    if appendedcontainernumbers == 0:
        appendlist = 1;
    else:
        appendlist = 0;

    return appendedContainer,appendlist
	
def fill_with_explicit(container):
    appendlist = 0
    while appendlist == 0:
        appendedContainer,appendlist = loop_process(container,appendlist)
        container = appendedContainer
        if appendlist == 1:
            appendedContainer,appendlist = loop_process(container,appendlist)        
    return appendedContainer
```

This functions will run previous functions in a sequence where, rows, columns and nonets are referenced. Any cell with only 1 number after checking for overlaps will be appended. We will run this functions as a loop to append cells until eventually the numbers are all filled up. 

The function will return a 9x9 container with appended numbers. The eventual puzzle is not yet solved and we have to move on to the next step of the solver.

## Step 2:
```
def impicit_solver_hor_vert(explicit_filled_container):
    pointer_y = 0
    pointer_x = 0
    pointer_x_2 = 0

    for pointer_y in range(row):
        overlap_master = set()
    
        for pointer_x in range(len(explicit_filled_container[pointer_x])):
            if type(explicit_filled_container[pointer_y][pointer_x]) == list:
                for pointer_x_2 in range(pointer_x + 1 , len(explicit_filled_container[pointer_x])):
                    if type(explicit_filled_container[pointer_y][pointer_x_2]) == list:
                        overlap = set(explicit_filled_container[pointer_y][pointer_x]) & set(explicit_filled_container[pointer_y][pointer_x_2])
                        overlap = list(overlap)                    
                        for num in range(len(overlap)):
                            overlap_master.add(overlap[num])            
        overlap_master = list(overlap_master)

        for pointer_x in range(len(explicit_filled_container[pointer_x])):
            
            if type(explicit_filled_container[pointer_y][pointer_x]) == list:
                for num in range(len(overlap_master)):
                    if overlap_master[num] in explicit_filled_container[pointer_y][pointer_x]: explicit_filled_container[pointer_y][pointer_x].remove(overlap_master[num])
                if len(explicit_filled_container[pointer_y][pointer_x]) == 1:
                    explicit_filled_container[pointer_y][pointer_x] = explicit_filled_container[pointer_y][pointer_x][0]
                else:
                    explicit_filled_container[pointer_y][pointer_x] = 0

    implicit_filled_container = list(explicit_filled_container)
    return implicit_filled_container
```

This function will reference the possible numbers from cells that are not yet filled in rows and then the columns. 

For example, in a row that have 3 cells that are still unfilled, we have possible numbers:
1. Cell 1: [1,3,6]
2. Cell 2: [2,3,6]
3. Cell 3: [1,2,3,6,9]

Base on elimination, we can see that the number in cell 3 is 9 as Cell 1 and 2 does not have the possibility of filling 9. 9 is not yet filled up and hence the only cell capable of having 9 is cell 3.

With this logic, the function will reference cell 1,2,3 and eliminate the array of possible numbers based on the other cell numbers. The cell that has eventually only 1 number left will be filled. 

## Main routine:
```
row = 9
col = 9

pointer_y = 0
pointer_x = 0
container = quizzes[80].tolist()
print('Empty Suduko Board:\n',np.asarray(container))
solution = solutions[80]

explicit_filled_container = fill_with_explicit(container)
implicit_filled_container_hor_filled = impicit_solver_hor_vert(explicit_filled_container)
implicit_filled_container_hor_filled = fill_with_explicit(implicit_filled_container_hor_filled)
t_container = list(map(list, zip(*explicit_filled_container)))
implicit_filled_container_vert_filled = impicit_solver_hor_vert(t_container)
implicit_filled_container_hor_and_vert_filled = list(map(list, zip(*implicit_filled_container_vert_filled)))
implicit_filled_container_hor_and_vert_filled = np.asarray(implicit_filled_container_hor_and_vert_filled)


print('Solved Suduko Board:\n',implicit_filled_container_hor_and_vert_filled)
print('Solution:\n',solution)
```

Running step 1 & 2 function in sequence, one after the next, will eventually fill up the all the cells in a 9x9 Sudoku puzzle.    	

  
