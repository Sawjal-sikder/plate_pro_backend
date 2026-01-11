from rest_framework.views import exception_handler #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework import status #type: ignore

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Validation errors
    if isinstance(response.data, dict):
        custom_data = {}
        for key, value in response.data.items():
            if isinstance(value, list) and value:
                # Take the first error message for each field
                custom_data[key] = value
            elif isinstance(value, str):
                custom_data[key] = value
            else:
                custom_data[key] = str(value)
        
        return Response(
            {
                "message": custom_data[next(iter(custom_data))][0] if len(custom_data) == 1 and isinstance(custom_data[next(iter(custom_data))], list) else "Validation error",
                "message_details": custom_data
            },
            status=response.status_code
        )

    return Response(
        {"message": "Something went wrong"},
        status=response.status_code
    )
    
    
    
    
#     from rest_framework.views import exception_handler #type: ignore
# from rest_framework.response import Response #type: ignore
# from rest_framework import status #type: ignore

# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)

#     if response is None:
#         return Response(
#             {"message": "Internal server error"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

#     # Validation errors
#     if isinstance(response.data, dict):
#         for key, value in response.data.items():
#             if isinstance(value, list) and value:
#                 # Take the first error message for the field
#                 return Response(
#                     {"message": value[0]},
#                     status=response.status_code
#                 )
#             elif isinstance(value, str):
#                 return Response(
#                     {"message": value},
#                     status=response.status_code
#                 )

#     return Response(
#         {"message": "Something went wrong"},
#         status=response.status_code
#     )
    
    
    