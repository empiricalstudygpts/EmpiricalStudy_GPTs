This is the github repository of paper 《An Empirical Study of the Security Vulnerabilities of GPTs》. The res.xlsx shows our results. Each column in the file corresponds to:

the names of GPTs in our experiments,

their leaked expert prompts, 

the names of their jit_plugins, 

the classification of the GPTs based on the components they have (0 means no tools or knowledge, 1 means only basic tools, 2 means only user-defined tools, 3 means basic tools + user-defined tools, 4 means tools + knowledge), 

the results of attacks on three basic tools: DALL·E, Python and browser,

the results knowledge injection attacks on three basic tools: DALL·E, Python and browser,

our proposed prompt-enhanced version of GPTs (E represents including expert prompt defensive tokens, C represents including components defensive tokens, K represents including defensive tokens of separating knowledge instructions).
