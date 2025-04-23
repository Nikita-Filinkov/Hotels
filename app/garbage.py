




# @router.post('/loging')
# async def loging_user(response: Response, user_date: SUserAuth):
#     user = await auth_user(email=user_date.email, password=user_date.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#
#     access_token = create_access_token({'sub': user.id})
#     response.set_cookie("booking_access_token", access_token, httponly=True)
#     return access_token