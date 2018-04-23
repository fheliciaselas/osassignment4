
import sys
import copy

input_file = 'input.txt'

buffer_time = 45

class Process:

    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.last_scheduled_time = arrive_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

    

def append_to_schedule(schedule,current_time, process_id):
   
    if len(schedule) > 0:
        last_schedule = schedule[n-1]
        previous_process_id = last_schedule[1]
        if process_id != previous_process_id:
            schedule.append((current_time, process_id))
    else:
        schedule.append((current_time, process_id))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time

def RR_scheduling(process_list, time_quantum):
    schedule = []
    current_time = 0
    waiting_time = 0
    Q_processing = []
    Q_unprocessed = copy.deepcopy(process_list)

    n = len(process_list)
    max_time = process_list[n-1].arrive_time + process_list[n-1].burst_time + buffer_time  #max time for simulation
    
    while current_time < max_time:
        while len(Q_unprocessed) > 0:
            todo = Q_unprocessed[0]
            if todo.arrive_time <= current_time+time_quantum:
                Q_processing.append(todo) # add to process list
                Q_unprocessed.pop(0) # remove from unprocessed list
            else:
                break

        if len(Q_processing) > 0:
            current_process = Q_processing[0]
            
            if current_process.arrive_time <= current_time:
                Q_processing.pop(0)
                
                if current_time < current_process.last_scheduled_time:
                    current_time = current_process.last_scheduled_time #update current time
                
                waiting_time = waiting_time + (current_time - current_process.last_scheduled_time); #add waiting time
                append_to_schedule(schedule, current_time, current_process.id)  # processing
                
                if current_process.burst_time > time_quantum:
                    current_time += time_quantum
                    current_process.burst_time -= time_quantum
                    current_process.last_scheduled_time = current_time
                    Q_processing.append(current_process)
                else:
                    current_time += current_process.burst_time
                    current_process.burst_time = 0
                    current_process.last_scheduled_time = current_time
            else:
                current_time += 1
        else:
            current_time += 1

    average_waiting_time = waiting_time / float(len(process_list))
    
    return schedule, average_waiting_time



def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    

if __name__ == '__main__':
    main(sys.argv[1:])
