# Central Processing Unit

CPUs are built by placing billions of microscopic transistors onto a single computer chip. Those transistors allow it to make the calculations it needs to run programs that are stored on the system’s memory. They’re effectively minute gates that switch on or off, thereby conveying the ones or zeros that translate into everything we do with the device, be it watching videos or writing an email.

**At its core, a CPU takes instructions from a program or application and performs a calculation**. The executed instruction, or calculation, can involve basic arithmetic, comparing numbers, performing a function, or moving numbers around in memory. Since everything in a computing device is represented by numbers, we can think of the CPU as a calculator that runs incredibly fast.

Today’s modern CPU consists of multiple cores that allow it to perform multiple instructions at once, effectively cramming several CPUs on a single chip.

<p align="center">
  <img width="600" height="250" img src="images/four_core_cpu.png">
</p>

The cores in this diagram are sharing something called the **L3 cache**. This is a form of onboard memory inside the CPU. CPUs also have **L1** and **L2** caches contained in each core, as well as registers, which are a form of low-level memory.

<br>

# Operating System

A computer's **operating system** (OS) manages all of the software and hardware on the computer. Most of the time, there are several different computer programs running at the same time, and they all need to access the computer's central processing unit (CPU), memory, and storage. The operating system coordinates all of this to make sure each program gets what it needs.

<br>

# Process

A **process** is the instance of a computer program that is being executed by one or many threads. This can be anything from a small background task, such as a spell-checker or system events handler to a full-blown application like Internet Explorer or Microsoft Word. All processes are composed of one or more threads. Put another way, a process is defined as an entity which represents the basic unit of work to be implemented in the system

A **program** is a piece of code which may be a single line or millions of lines. A computer program is usually written by a computer programmer in a programming language. For example, a simple program written in C programming language:

```C
#include <stdio.h>

int main() {
   printf("Hello, World! \n");
   return 0;
}
```

A computer program is a collection of instructions that performs a specific task when executed by a computer. **When we compare a program with a process, we can conclude that a process is a dynamic instance of a computer program.**

<br>

# Thread

A **thread** is a flow of execution through the process code, with its own program counter that keeps track of which instruction to execute next, system registers which hold its current working variables, and a stack which contains the execution history.

**Each thread belongs to exactly one process and no thread can exist outside a process. Each thread represents a separate flow of control.** However, a process can have multiple threads.

<br>

<p align="center">
  <img width="600" height="350" img src="images/threads.png">
</p>

A thread shares with its peer threads few information like **code segment**, **data segment** and **open files**. When one thread alters a code segment memory item, all other threads see that.

<br>

| **Process**                                                                                                         | **Thread**                                                                         |
|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Process is heavy weight or resource intensive.                                                                      | Thread is light weight, taking lesser resources than a process.                    |
| Process switching needs interaction with operating system.                                                          | Thread switching does not need to interact with operating system.                  |
| In multiple processing environments, each process executes the same code but has its own memory and file resources. | All threads can **share** same set of open files, child processes.                     |
| If one process is blocked, then **no other process can execute until the first process is unblocked**.                  | While one thread is blocked and waiting, a second thread in the same task can run. |
| Multiple processes without using threads use more resources.                                                        | Multiple threaded processes use fewer resources.                                   |
| In multiple processes each process operates **independently** of the others.                                            | One thread can read, write or change another thread's data.                        |

<br>

# Asynchronous V.S. Synchronous

**Asynchronous programming**, conversely, is a multi-threaded model where tasks can run concurrently without waiting for other tasks to complete. Asynchronous is a non-blocking architecture, which means it doesn’t block further execution while one or more operations are in progress.

**Synchronous** is known as a blocking architecture. As a single-threaded model, it follows a strict set of sequences, which means that operations are performed one at a time, in perfect order. While one operation is being performed, other operations’ instructions are blocked. The completion of the first task triggers the next, and so on.
