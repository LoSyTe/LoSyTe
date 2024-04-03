# DeLoSo
## [Logic Synthesis Tools Testing via Configuration Diversification with Combinatorial Multi-Armed Bandit](https://github.com/LoSyTe/LoSyTe)
**The logic synthesis tools we tested include:**
1. **Commercial Logic Synthesis Tool Vivado (latest version 2023.1 and 2023.2)**
2. **Open Source Logic Synthesis Tool Yosys (latest version 0.30 + 48)**
***

**Env dependencies:**
1. **Vivado 2023.1 and 2023.2**
2. **Yosys 0.30 + 48**
3. **Icarus Verilog 13.0**
4. **Verismith 1.0.0.2**
5. **python 3.8**
6. **GHC 8.6.5**
7. **Cabal 3.6.0**
8. **Stack 2.9.3**
9. **HLS 2.0.0.1**
***

### Our Works
The complexity of circuit design continues to increase. It becomes particularly crucial to ensure the accuracy and reliability of logic synthesis tools. These tools efficiently convert hardware description languages into optimized gate-level netlists. However, inherent faults may cause failures in the synthesis process, which affects the accuracy of the generated netlists. In traditional approaches, the testing of logic synthesis tools has predominantly depended on code generators for test-program generation. However, the success of these methods is significantly influenced by the suitability of generator configurations. For an effective test configuration, it must produce test programs that are both bug-revealing (i.e., capable of triggering bugs) and diverse (i.e., ensuring the detection of various bug types). To achieve this goal, we propose LoSyTe: Logic Synthesis Tools Testing via Configuration Diversification with Combinatorial Multi-Armed Bandit. LoSyTe conducts comprehensive testing of logic synthesis tools through dynamic optimization of test-program generator configurations. It consists of three main components. Configuration selection component applies a multi-armed bandit algorithm to select and optimize configuration combinations based on test feedback. Test-program vectorization component turns test-programs into feature vectors to quantify test diversity. Equivalence checking component checks the consistency of synthesized netlists with Verilog tests, to identify synthesis faults and guide strategy adjustments. We assess LoSyTe on both proprietary commercial logic synthesis tools (i.e., Vivado)  and open-source logic synthesis tools (i.e., Yosys). The results show that LoSyTe successfully discovered 20 bugs of 4 types; all the reported bugs have been confirmed or fixed by developers.

***
### Main File
Our methodology is located in the 'method' directory:

1.DeLoSoforVivado folder:

This folder includes DeLoSoforVivado.py and DeLoSoforVivado_main.py files. DeLoSoforVivado.py comprises our LSOC (Loop Structure Obfuscation Criteria) generator and LSOC diversity evaluator, while DeLoSoforVivado_main.py incorporates the LSOC validator. The main function is also embedded in DeLoSoforVivado_main.py. By assigning the actual test case path to the variable 'files_path' in line 38 and executing the DeLoSoforVivado_main.py file, we can conduct testing on optimization bugs in Vivado. 

2.DeLoSoforYosys folder:

This folder contains DeLoSoforYosys.py and DeLoSoforYosys_main.py files. Similarly, by executing the DeLoSoforYosys_main.py file, we can conduct testing on optimization bugs in Yosys.

3.baseline folder:

This folder contains the implementations of the three comparison algorithms used in the baseline of this paper, which are Default, InitSwarm, and DynSwarm. 

4.example folder:

This folder contains two test cases automatically generated using the Verismith tool. In our experiments, all test cases are program codes generated through the Verismith tool.

5.optimization bugs folder:

This folder encompasses optimization bugs discovered in the Vivado and Yosys logic synthesis tools. Each bug file includes a bug_description.pdf, providing details on the triggering conditions and an explanation of the bug issues.
***

### Here are the details of these bugs
These errors in the error file can be reproduced using Vivado 2023.1, 2023.2 and Yosys 0.30+48.

You can find all bug files in path `method/optimization bugs`.

Fault1：vivado	7BrmgwSAB	 HARTHOptPost::optimize() function triggers a crash during Vivado synthesis.

Fault2：vivado	7jBos5SAC  Synthesis failure due to an unexpected fault in the HARTGLAddGen() function.

Fault3：vivado	7jBooqSAC	 Error invoking Tcl\_Panic function, triggering synthesis termination.

Fault4：vivado	7mhiM4SAI	 Synthesis failure is encountered as a consequence of a crash initiated by the NBaseModC::realModule()function.

Fault5：vivado	7hvpQPSAY	 The HARTOptMux::findEnc() function triggers a Vivado crash, resulting in synthesis failure.

Fault6：vivado	7HkoVvSAJ	 The HARTNDb::elaborate function triggered a Vivado crash, causing the synthesis to fail.

Fault7：vivado	7k0SoLSAU	 Vivado synthesis failure is attributed to a crash triggered by the ConstProp::evaluate() function.

Fault8：vivado	7k0StYSAU	 The NPinC::parentModule() function is causing Vivado to crash.

Fault9：vivado	7lpEt6SAE	 Vivado synthesis is hitting a roadblock with a crash initiated by the HARTHOptPost::prepDsps() function.

Fault10：vivado	7rbE4ISAU	 Vivado Synthesis Crashes and Unable to Locate Problematic Function in Log Files.

Fault11：vivado	7lRrQrSAK	 The HARTNDb::constProp() function is provoking a Vivado crash.

Fault12：vivado	7yJmiPSAS	 Vivado Synthesis Crashes and Unable to Locate Problematic Function in Log Files.

Fault13：vivado	7p4vsSSAQ	 Synthesis is failing due to an fault within the DFNode::findDFPin() function.

Fault14：vivado	7iVNTSSA4	 When synthesizing, an fault occurs in the SPinArray::createBus() function.

Fault15：vivado	7lRrQrSAK	 The exception in the HRTInvoker::inProcessLaunch() function results in synthesis failure.

Fault16：vivado	7ZIdXVSA1	 Inconsistent Simulation Results Due to Logic Synthesis Optimization Issue.

Fault17：yosys	   4079	   Issue in Yosys Synthesis: 'std::length\_fault' Leads to Termination.

Fault18：yosys	   4056	   Long runtime and high memory usage for synth.

Fault19：yosys	   4071	   Assertion Failure in AST Processing during Verilog Synthesi.

Fault20：yosys	   4077	   Yosys Verilog Parsing fault: Issue in AST Generation.
***
**We've had so much help from Vivado and Yosys staff in finding and confirming bugs. I would like to express my gratitude here.**
