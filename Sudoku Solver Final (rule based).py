# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 23:36:39 2020

@author: allen
"""

import numpy as np
quizzes = np.zeros((100, 81), np.int32)
solutions = np.zeros((100, 81), np.int32)
for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:100]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s
quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))

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

    
