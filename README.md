# business-innovations-interview
Case study and exercises for Business Innovations Associate

TUBURA

_Last updated: 29 May 2019_

**Case study: PIN codes**

_ _

_I. Context_

The TUBURA program is in the process of experimenting large-scale mobile services on USSD, including an ongoing trial involving enrolling clients and processing client orders via USSD systems. In the last year, more than 50,000 users have interacted with TUBURA mobile services, and this is expected to grow to over 150,000 users in the next year. Currently, in order to access our mobile services, users only need to supply their _Account Number_, a unique number generated by TUBURA and supplied to our clients through our field officers.

As part of TUBURA&#39;s goal of protecting our client&#39;s data and reducing the potential for fraud, the new Business Innovations and Analytics team will be integrating PIN codes into all existing and new USSD services. This means that in order to access our mobile services, our clients will be required to provide both their account number and a PIN code. While this will provide enhanced security for our clients and our services, it will likely be complex and challenging to train our clients.

_II. Task_

Develop a plan for the integration of PIN codes into our mobile services for all clients. In this plan, include the following:

- Dates of rollout, and the reasoning behind that choice
- Structure of rollout - should the roll-out be staggered by region or district, or should the new requirement be applied to all clients at once
- Impact on clients and on the country program
- Major risks associated with this rollout, and what steps can be taken to ameliorate them

In developing this plan, you&#39;ll want to consult with TUBURA employees at HQ. You&#39;ll also want to map existing mobile services, including all USSD and 2-way SMS services. (Are there any services that wouldn&#39;t need a pin). Critical teams to consult with include Field Ops, Customer Engagement, and Innovations Phase 3.

_Deliverables_

1. Document (PowerPoint presentation, Google Document, or other) outlining your plan. Include all of the points listed above
2. Brief (half-page or less) reflection on process. Who did you speak to? What was challenging about this project? What more would you need to learn to implement your plan?



**Exercise 1: Tool creation**

Using the tool (Python, R, Excel macro / VBA, Julia, or other) of your choice, write a script or macro to convert _input.csv_ into the format found in _out-format.json_, both in the exercise-1 folder. A completed version of the output can be found in the same folder, under the name _output.json_.

Note: for this exercise, while a working tool would be the preferred deliverable, it is not required. In attempting to solve this problem, we&#39;re more interested in your process and your approach to solving new problems with new tools. In working on this exercise, keep track of _how_ you approached the problem. What resources did you use? What did you Google? What new did you learn?

_Deliverables_

1. Data conversion tool, if possible
2. Process documentation, in whatever form you find appropriate or useful to share. This will be a major point of discussion during the interview, so be ready to discuss!



**Exercise 2: Code comprehension and documentation**

In the _exercise-2_ folder, you&#39;ll find a Python file called _pnseb-allocation-tool.py_, and an input file named pnseb-input.xlsx. Review the code, run the file on the input, and save the output. In order to successfully run the code, you may have to make a few changes to the Python script, the input file, or both.

_Deliverables_

1. **1.** Short write-up (half-page or less) of what this program does.
2. **2.** Output from the program
3. **3.**** Bonus**: comment the code, including your changes!

_Note_: this exercise will require that you have Python 3.6 or greater and pandas 0.24 or greater installed on your system. I recommend the Anaconda3 distribution of Python, which comes with pandas included. (If you have Anaconda already installed on your system, you may want to update both your version of Python and of pandas. In most cases, using the command **conda update -n root conda** followed by **conda update --all** in the command prompt will update Anaconda, Python, and most needed modules.)
