
.PHONY: clean 

all: minishell

MINISHELL_VERSION=\"2017.1\"
ARCH_LIB_DIR=lib/$(shell uname -ms | tr ' ' '/')

minishell: minishell.o minishell_input.o 
	gcc -ggdb -Wall -o minishell minishell.o minishell_input.o -L${ARCH_LIB_DIR} -lshell 

minishell.o: minishell.c minishell_input.h internals.h execute.h jobs.h
	gcc -ggdb -Wall -c -o minishell.o minishell.c

minishell_input.o: minishell_input.c minishell_input.h
	gcc -ggdb -Wall -c -o minishell_input.o minishell_input.c

jobs.o: jobs.c jobs.h
	gcc -ggdb -Wall -DMINISHELL_VERSION=$(MINISHELL_VERSION) -c -o jobs.o jobs.c

internals.o: internals.c internals.h
	gcc -ggdb -Wall -DMINISHELL_VERSION=$(MINISHELL_VERSION) -c -o internals.o internals.c

clean:
	rm -rf minishell *.o

