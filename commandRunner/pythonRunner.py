import os
import re
import types
from commandRunner import commandRunner
from subprocess import call


class pythonRunner(commandRunner.commandRunner):

    def __init__(self, **kwargs):
        script = ""
        if isinstance(kwargs['script'], str):
            self.script = kwargs.pop('script', '')
        else:
            raise TypeError('script must be a string')

        commandRunner.commandRunner.__init__(self, **kwargs)

    def run_cmd(self, success_params=[0]):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        exit_status = None
        os.chdir(self.path)
        try:
            if self.env_vars:
                # print("USING ENVS!!!")
                exit_status = call(self.command, shell=True, env=self.env_vars)
            else:
                exit_status = call(self.command, shell=True)
        except Exception as e:
            raise OSError("call() attempt failed")

        output_dir = os.listdir(self.path)

        if exit_status not in success_params:
            raise OSError("Exit status " + str(exit_status))

        self.output_data = {}
        for this_glob in self.out_globs:
            for outfile in output_dir:
                if outfile.endswith(this_glob):
                    with open(self.path+outfile, 'rb') as content_file:
                        self.output_data[outfile] = content_file.read()

        return(exit_status)