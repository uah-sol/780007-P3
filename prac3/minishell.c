#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>

#include "execute.h"
#include "parser.h"
#include "minishell_input.h"

void show_command(command * p_cmd);

int main (int argc, char *argv[])
{
    command* cmds;
    char* raw_command;
    int n_cmds=0;
    int n, i;

    while (1)
    {
        // We print the prompt 
        print_prompt(); 
 
        raw_command = NULL;
        n = read_line (&raw_command, stdin);
        if (n==-1) 
        {
            break;
        }

        n_cmds = parse_commands(&cmds, raw_command); 

        for (i = 0; i < n_cmds; i++)
        {
            show_command(&cmds[i]);
        }

        free_commands(cmds, n_cmds); 
        free(raw_command);
    }

    exit(0);
}

void show_command(command * p_cmd)
{
    int i;

    printf ("\tRaw command: \"%s\"\n", p_cmd->raw_command);
    printf ("\tNumber of arguments: %d\n", p_cmd->argc);

    for (i=0; i<=p_cmd->argc; i++)
        if (p_cmd->argv[i] != NULL)
            printf ("\t\targv[%d]: \"%s\"\n", i, p_cmd->argv[i]);
        else
            printf ("\t\targv[%d]: NULL\n", i);

    if (p_cmd->input)
        printf ("\tInput: \"%s\"\n", p_cmd->input);

    if (p_cmd->output)
        printf ("\tOutput: \"%s\"\n", p_cmd->output);

    if (p_cmd->output_err)
        printf ("\tError output: \"%s\"\n", p_cmd->output_err);

    printf ("\tExecute in the background: %s\n",
            p_cmd->background ? "Yes" : "No");
}
