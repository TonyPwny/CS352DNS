This starter code is to let you explore the socket programming interface in
and some other basic aspects of the Python language.

This exercise will serve as the foundation for the upcoming programming
projects. A sample working code is given to you in proj0.py. The program consists
of server code and client code written as two separate threads.

(1) Understand the functionality implemented in the program. First, download,
    save and execute the program as is in your environment. Make sure it executes
    successfully and according to how you would expect.

Then attempt the changes suggested below. This project isn't graded, but it will
help subsequent projects if you try playing around with the program as follows.

(2) Try running the program immediately again when it finishes
    successfully. What do you see? Why? What happens when you remove the various
    sleep()s in the program?

(3) Separate the server code and client code into two different programs,
    server.py and client.py. Execute the server program first and then execute
    the client program. You should still get the same set of print messages as
    in the combined threaded code (proj0.py)

(4) In the given code, the server just sends a message string to the client
    after it connects. Modify the program so that the client sends a string to
    the server and then the server reverses the string and sends it back to the
    client. If the client sends "HELLO" to the server, the client should receive
    "OLLEH". Your program should print the string sent by the client and the
    corresponding string received by the client. Your client program should be
    able to read a string (each line is a string) from a test file (say,
    in-proj0.txt). Similarly, the output of your program should be written to a
    file (say, out-proj0.txt).
