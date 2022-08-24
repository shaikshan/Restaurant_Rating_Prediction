import os, sys

class RestaurantException(Exception):
    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message = RestaurantException.get_detailed_error_message(error_message=error_message,
                                                                            error_detail=error_detail)
                                                                            
       


    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys):
        """
        error_message: Exception object
        error_detail: sys object
        """

        _,_,exec_tb = error_detail.exc_info()
        line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error occured in script:[{file_name}] at line number:[{line_number}] error_message:[{error_message}]"
        return error_message

    def __str__(self) -> str:
        return self.error_message

    def __repr__(self) -> str:
        return RestaurantException.__name__.str()


