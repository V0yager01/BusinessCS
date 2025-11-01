from fastapi import status, HTTPException


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},)


auth_exception = HTTPException(detail='Invalid login or password',
                               status_code=status.HTTP_401_UNAUTHORIZED)
register_exception = HTTPException(detail='Email is already in use',
                                   status_code=status.HTTP_400_BAD_REQUEST)

authorize_exception = HTTPException(detail='You do not have permission to access this resource',
                                   status_code=status.HTTP_403_FORBIDDEN)

json_exception = HTTPException(detail='Invalid json parameters',
                               status_code=status.HTTP_400_BAD_REQUEST)

exception_404 = HTTPException(detail='Task does not exist',
                               status_code=status.HTTP_404_NOT_FOUND)