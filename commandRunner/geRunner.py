import os
import re
import types
import drmaa
from commandRunner import commandRunner


class geRunner(commandRunner.commandRunner):

    def __init__(self, **kwargs):
        commandRunner.commandRunner.__init__(self, **kwargs)

    def _translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # interpolate the file names if needed
        if self.output_string is not None:
            command = command.replace("$OUTPUT", self.output_string)
        if self.input_string is not None:
            command = command.replace("$INPUT", self.input_string)
        return(command)
        
    def prepare(self):
        '''
            Makes a directory and then moves the input data file there
        '''
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if self.input_data is not None:
            for key in self.input_data.keys():
                file_path = self.path+key
                fh = open(file_path, 'w')
                fh.write(self.input_data[key])
                fh.close()

    def run_cmd(self, success_params=[0]):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        exit_status = None
        try:
            jt = s.createJobTemplate()
            jt.remoteCommand = os.path.join(os.getcwd(), 'sleeper.sh')
            jt.joinFiles = True

            jobid = s.runJob(jt)

            retval = s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)

            s.deleteJobTemplate(jt)
        except Exception as e:
            raise OSError("DRMAA session failed to execute")
        #
        # if exit_status in success_params:
        #     if os.path.exists(self.out_path):
        #         with open(self.out_path, 'r') as content_file:
        #             self.output_data = content_file.read()
        # else:
        #     raise OSError("Exist status" + str(exit_status))
        return(exit_status)

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the tjmp dir
        '''
        for this_file in os.listdir(self.path):
            file_path = os.path.join(self.path, this_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        if os.path.exists(self.path):
            os.rmdir(self.path)