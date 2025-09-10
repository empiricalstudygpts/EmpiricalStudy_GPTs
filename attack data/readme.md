# result.csv

The result.xlsx shows our results of information leakage attack. Each column in the file corresponds to:

the URL of GPTs in our experiments,

the attack prompt of basic expert prompt leakage,

their leaked expert prompts, 

the attack success rate (ASR) of basic expert prompt leakage,

the category of the GPTs based on the components they have (0 means no tools or knowledge, 1 means only basic tools, 2 means only user-defined tools, 3 means basic tools + user-defined tools, 4 means tools + knowledge), 

if the GPTs is equipped with DALL·E (1 means yes),

if the GPTs is equipped with Python (1 means yes),

if the GPTs is equipped with Web Browser (1 means yes),

the attack prompt of basic component leakage,

the names of their jit_plugins (if have), 

the names of their knowledge files (if have).

# result_form_variants.csv

The result form variants.xlsx shows our results of information leakage attack variants. 

'gpts_url': the URL of GPTs that we are unable to get the expert prompts through basic attack,

'prompt': the expert prompt we obtain through attack variants,

1 means the attack variant is successful.