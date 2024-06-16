import sys
from src.logger import logging 
def error_handling(error,error_object:sys):
    _,_,err_track=error_object.exc_info()
    file_name=err_track.tb_frame.f_code.co_filename
    # errror_message="Error occured in the Script [{0}] in the line number [{1}] the Error is [{2}]".format(file_name,err_track.tb_lineno,error)
    error_message = "Error occurred in the Script [{0}] in the line number [{1}] the Error is [{2}]".format(file_name, err_track.tb_lineno, error)
    return error_message


class Customexception(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_handling(error_message,error_detail)

    def __str__(self):
        print(self.error_message)
        logging.info(self.error_message)
        return self.error_message

