import json
import time
import threading
import io
import sys
import unittest
  
class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""

        elapsed_time = time.perf_counter() - self._start_time
        # self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.0f} seconds")
    

def find_start(dag):
    """
    find the starting node
    """
    for key in dag:
        if "start" in dag[key]:
            return key
      
def print_nodes(i):
    print ('printing nodes',i)

def print_edges(i):
    print ('printing edges',i)
               
def runner(json_file):
    """
    takes a json file, turns into python dictionary, and print out nodes and its children at given time given. 
    Utilizing BFS approach, runner goes through the tree and create timer threads for each node and its children. 
    children will get then get appended to a queue. 
    All threads coming from the same node will start once they are created and 
    join each other after they start. 
    The same node will not be visited twice

    Timer is used to measure second passed. 
        
    """

    f1 = open(json_file,)
    dag = json.load(f1)
    f1.close()
    
    if len(dag) == 1:
        print(print_nodes(find_start(dag)))
        return 
    visited = set()
    queue = [find_start(dag)]  

    while queue:
        current = queue.pop(0)
        visited.add(current)
        timer = Timer()
        timer.start()
        
        if dag[current]['edges']:  #if node has children

            t = threading.Timer(0,print_nodes,[current])  
            thread_list = [t]

            for key in dag[current]['edges']:
               
                if key not in visited:
                    queue.append(key)
                    visited.add(key)

                    time = dag[current]['edges'][key]
                    
                    edges = threading.Timer(time,print_edges,[key])
                    thread_list.append(edges)

            for i in thread_list:
                i.start()
            for i in thread_list:
                i.join()
                timer.stop()
      
  
class TestRunner(unittest.TestCase):

    def test0(self):
        '''testing stdoutput in console with example0'''
        capturedOutput = io.StringIO()         
        sys.stdout = capturedOutput

        runner('testcase0.json')

        sys.stdout = sys.__stdout__                  
        # print (capturedOutput.getvalue()) 
        expected = '''printing nodes A\nNone'''
        output = capturedOutput.getvalue().strip() # Now works as before.
        message = "First value and second value are not equal !"
        self.assertEqual(expected, output, message)

    
    def test1(self):
        '''testing stdoutput in console with example1'''
        capturedOutput = io.StringIO()         
        sys.stdout = capturedOutput

        runner('testcase1.json')

        sys.stdout = sys.__stdout__                  
        # print (capturedOutput.getvalue()) 
        expected = '''printing nodes A
Elapsed time: 0 seconds
printing edges B
Elapsed time: 2 seconds
printing edges C
Elapsed time: 3 seconds'''
        output = capturedOutput.getvalue().strip() # Now works as before.
        message = "First value and second value are not equal !"
        self.assertEqual(expected, output, message)

    def test2(self):
        '''testing stdoutput in console with example2'''
        capturedOutput = io.StringIO()         
        sys.stdout = capturedOutput

        runner('testcase2.json')

        sys.stdout = sys.__stdout__                  
        expected = '''printing nodes A
Elapsed time: 0 seconds
printing edges B
Elapsed time: 1 seconds
printing edges C
Elapsed time: 2 seconds
printing nodes B
Elapsed time: 0 seconds
printing edges D
Elapsed time: 1 seconds
printing edges E
Elapsed time: 2 seconds
printing nodes C
Elapsed time: 0 seconds
printing nodes D
Elapsed time: 0 seconds'''
        output = capturedOutput.getvalue().strip() # Now works as before.
        message = "First value and second value are equal !"
        self.assertEqual(expected, output, message)
  

  
if __name__ == '__main__':
    # unittest.main()
    runner('testcase0.json')
    print('end of test0')
    runner('testcase1.json')
    print('end of test1')
    runner('testcase2.json')
    print('end of test2')
    