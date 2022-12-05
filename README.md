# Proejct Description: The Transport Layer and ARQ Implementation


In this project, I have implemented two well-known ARQ protocols, stop and wait and selective repeat. As these protocols are wellknown in the computer network community, there is no need for further discussion. Instead, here we will denote some implementation facets.

### Segments and Acks Structure
1.	Sequence number:  
  a.	For Stop and Wait 1-bit.  
  b.	For Selective Repeat 32-bit  
2.	16-bit as segment indicator, which is 0101010101010101
3.	16-bit as ack indicator, which is 1010101010101010
4.	16-bit checksum in both segments and acks
5.	Payload with a variable size, which we will denote as MSS


### Stop and Wait Specification
Stop and wait ARQ has multiple variations, but we have implemented the most advanced version in this project. The sender FSM of this stop and wait ARQ is introduced in figure 3.15 as rdt3.0 (page 245 of the reference book, computer networks: a top down approach. Edition 6). By looking at this FSM, we can see that this ARQ encounters noisy channels that packets can be lost or corrupted while passing through it.
Summary of specifications:
1. we have Used timers for handling packet loss
2. we have Used checksum to check whether receiving packet/ack is corrupted or not.
3. we have Used sequence number as its obvious why.
4. Added segment indicator to segments.
5. Added ack indicator to acks.


### Selective Repeat Specification
As it is known, this ARQ is far more effective than stop and wait ARQ. Everything seems good in theory about this ARQ, but it can be challenging to implement it in practice. To implement selective repeat, you have to be familiar with threads and deal with condition races.

### Simulation and Results
1. Simulate packet loss with a probability of P. we receive a P (where 0≤P≤1) from the command line (as one of your arguments). Then, upon receiving packets in the receiver, generate a random number 0≤r≤1. Whenever r≤P discard the received packet.
2. Alter one bit (choose this randomly) with the probability of 0.01 at sender using the exact mechanism as the above statement.
3. we have prepared average results for this project. For each of the following parts, you have to repeat the simulation five times, then report the average of those iterations in your report.
  a. Simulate delay over MSS. MSS starts from 100-bytes and goes up to 1000-bytes in 100-bytes steps.  
  b. Simulate delay over window size. Window size starts from 1 and goes up to 64 doubling at each step.  
  c. Simulate delay over P. P starts from 0 and goes up to 0.2, and increases by 0.01 at each step.  
7. we have Ploted the result of the simulations and included them in the work report.


### Implementations Note
1. we have Used UDP for both cases.
2. we can send a file over these ARQs. (a generated a simple text file).
3. Window size, MSS, P, and filename can be optain from arguments but it is not necessary
