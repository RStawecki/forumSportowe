import datetime

actualDate = datetime.datetime.now()
print(actualDate)
createdDate = datetime.datetime(2021,3,8,20,13,00)
print(createdDate)
#diffDate = actualDate - createdDate
diffDate = (actualDate - createdDate).total_seconds()
print(abs(diffDate))
#totalSeconds = diffDate.total_seconds()
#print(totalSeconds)
print(24*60*60)
if(diffDate >= 86400):
    print(round(diffDate/60/60/24), "d. ago")
elif(diffDate > 3600 and diffDate < 86400):
    print(round(diffDate/60/60), "h. ago")
else:
    print(round(diffDate/60), "min. ago")


