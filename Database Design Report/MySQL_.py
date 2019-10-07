#-*- coding: utf-8 -*-
#!/usr/bin/python
import mysql.connector
from mysql.connector import errorcode
import string, random
import time

#20144456 오영은이 팀플하려고 작성함

DB_ID = '여기에 DB 아이디를 입력해주세요'
DB_PASSWORD = '여기에 DB 비밀번호를 입력해주세요'

MAX_LOOP = 30;
HOSPITAL_MANY = 20;
DOCTOR_MANY=50;

SUBJECT_MANY=20;
NURSE_MANY=30;
SUBJECTLIST_MANY=16;
USER_MANY=30;
OFFICE_MANY=50;
ROOMNUMBER_MANY=20;
index=1;

DB_NAME = 'DBTeamProject'
hospitalID_array=[]
subjectID_array=[]
userID_array=[]
nurseID_array=[]
doctorID_array=[]
office_array=[]
roomNumber_array=[]
subject_name_array = ['소아과', '내과', '외과', '성형외과', '정신과', '비뇨기과', '피부과', '정형외과', '이비인후과',
'치과', '김성민과', '군병원', '암센터', '신경과', '방사선과', '산부인과']



""" Connect to MySQL database """
try:
    conn = mysql.connector.connect(host='localhost',
                                   database='DBTeamProject',
                                   user=DB_ID,
                                   password=DB_PASSWORD)
    cursor = conn.cursor()
    if conn.is_connected():
        print('Connected to MySQL database')
        cursor.execute("DROP DATABASE DBTeamProject")
        print "drop complete"
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print "create complete"
        cursor.execute("USE DBTeamProject")
except:
    print "Not Exist DB. I will Create a new DB..."
    conn = mysql.connector.connect(host='localhost',
                                   user=DB_ID,
                                   password=DB_PASSWORD)
    cursor = conn.cursor()
    if conn.is_connected():
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        cursor.execute("USE DBTeamProject")



def create_tables():
    TABLES = {}
    TABLES['User'] = (
        "CREATE TABLE `User`("
        	"`ID` CHAR(5) not null,"
        	"`password` VARCHAR(10) not null,"
        	"`name` VARCHAR(10),"
        	"`birthday` DATE,"
        	"`address` VARCHAR(10),"
        	"`phone` CHAR(11),"
        	"`phoneFamily` CHAR(11),"
        	"`gender` VARCHAR(6) not null,"
        	"`bloodType` VARCHAR(2),"
        	"`myRank` VARCHAR(10),"
        	"PRIMARY KEY (`ID`)"
            ") ENGINE=InnoDB")

    TABLES['Hospital'] = (
        "CREATE TABLE `Hospital`("
        	"`hospitalID` CHAR(5) not null,"
        	"`hospitalName` VARCHAR(10),"
        	"`location` CHAR(11),"
        	"PRIMARY KEY (`hospitalID`)"
            ") ENGINE=InnoDB")

    TABLES['Doctor'] = (
        "CREATE TABLE `Doctor`("
            "`doctorID` CHAR(5) not null,"
            "`hospitalID` CHAR(5) not null,"
            "`name` VARCHAR(10) not null,"
            "`birthday` DATE,"
            "`gender` VARCHAR(6) not null,"
            "`subjectID` CHAR(5) not null,"
            "`myRank` VARCHAR(10),"
            "PRIMARY KEY (`doctorID`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`),"
            "foreign key (`subjectID`) references `Medical_subject_list`(`subjectID`)"
            ") ENGINE=InnoDB")

    TABLES['Nurse'] = (
        "CREATE TABLE `Nurse`("
            "`nurseID` CHAR(5) not null,"
            "`hospitalID` CHAR(5) not null,"
            "`name` VARCHAR(10) not null,"
            "`birthday` DATE,"
            "`gender` VARCHAR(6) not null,"
            "`myRank` VARCHAR(10),"
            "PRIMARY KEY (`nurseID`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`)"
            ") ENGINE=InnoDB")

    TABLES['Medical_subject_list'] = (
        "CREATE TABLE `Medical_subject_list`("
        	"`subjectID` CHAR(5) not null,"
        	"`subjectName` VARCHAR(10),"
        	"PRIMARY KEY (`subjectID`)"
            ") ENGINE=InnoDB")

    TABLES['Medical_subject'] = (
        "CREATE TABLE `Medical_subject`("
        	"`hospitalID` CHAR(5) not null,"
        	"`subjectID` CHAR(5) not null,"
        	"PRIMARY KEY (`hospitalID`, `subjectID`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`),"
            "foreign key (`subjectID`) references `Medical_subject_list`(`subjectID`)"
            ") ENGINE=InnoDB")




    for name, ddl in TABLES.iteritems():
        try:
            #cursor.execute("DROP TABLE IF EXISTS ".join(name))
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")




def create_tables01():
    TABLES01 = {}
    TABLES01['OfficeBuilding'] = (
        "CREATE TABLE `OfficeBuilding`("
        	"`hospitalID` CHAR(5) not null,"
        	"`subjectID` CHAR(5) not null,"
            "`office` VARCHAR(5) not null,"
            "`roomNumber` VARCHAR(5) not null,"
            "`doctorID` CHAR(5) not null,"
        	"PRIMARY KEY (`hospitalID`, `office`, `roomNumber`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`),"
            "foreign key (`subjectID`) references `Medical_subject_list`(`subjectID`),"
            "foreign key (`doctorID`) references `Doctor`(`doctorID`)"
            ") ENGINE=InnoDB")

    TABLES01['Favorite'] = (
        "CREATE TABLE `Favorite`("
        	"`doctorID` CHAR(5) not null,"
        	"`userID` CHAR(5) not null,"
            "PRIMARY KEY (`doctorID`, `userID`),"
            "foreign key (`doctorID`) references `Doctor`(`doctorID`),"
            "foreign key (`userID`) references `User`(`ID`)"
            ") ENGINE=InnoDB")

    TABLES01['Support'] = (
        "CREATE TABLE `Support`("
        	"`hospitalID` CHAR(5) not null,"
        	"`userID` CHAR(5) not null,"
            "`totalMoney` INTEGER,"
        	"PRIMARY KEY (`hospitalID`, `userID`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`),"
            "foreign key (`userID`) references `User`(`ID`)"
            ") ENGINE=InnoDB")

    TABLES01['Distance'] = (
        "CREATE TABLE `Distance`("
        	"`ownerID` CHAR(5) not null,"
        	"`hospitalID` CHAR(5) not null,"
            "`distance` INTEGER,"
        	"PRIMARY KEY (`hospitalID`, `ownerID`),"
            "foreign key (`ownerID`) references `User`(`ID`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`)"
            ") ENGINE=InnoDB")

    TABLES01['Review_doctor'] = (
        "CREATE TABLE `Review_doctor`("
        	"`doctorID` CHAR(5) not null,"
        	"`userID` CHAR(5) not null,"
            "`score` INTEGER,"
        	"PRIMARY KEY (`doctorID`, `userID`),"
            "foreign key (`doctorID`) references `Doctor`(`doctorID`),"
            "foreign key (`userID`) references `User`(`ID`)"
            ") ENGINE=InnoDB")

    TABLES01['Review_hospital'] = (
        "CREATE TABLE `Review_hospital`("
        	"`hospitalID` CHAR(5) not null,"
        	"`userID` CHAR(5) not null,"
            "`score` INTEGER,"
        	"PRIMARY KEY (`hospitalID`, `userID`),"
            "foreign key (`hospitalID`) references `Hospital`(`hospitalID`),"
            "foreign key (`userID`) references `User`(`ID`)"
            ") ENGINE=InnoDB")

    TABLES01['Smartband'] = (
        "CREATE TABLE `Smartband`("
        	"`ownerID` CHAR(5) not null,"
        	"`location` CHAR(8),"
            "`temperature` FLOAT(4,1),"
            "`heartRate` INTEGER,"
            "`bloodPressure` INTEGER,"
        	"PRIMARY KEY (`ownerID`),"
            "foreign key (`ownerID`) references `User`(`ID`)"
            ") ENGINE=InnoDB")

    TABLES01['Appointment_table'] = (
        "CREATE TABLE `Appointment_table`("
        	"`doctorID` CHAR(5) not null,"
        	"`patientID` CHAR(5) not null,"
            "`appoint_time` DATETIME not null,"
        	"PRIMARY KEY (`doctorID`, `patientID`, `appoint_time`),"
            "foreign key (`doctorID`) references `Doctor`(`doctorID`),"
            "foreign key (`patientID`) references `User`(`ID`)"
            ") ENGINE=InnoDB")


    for name, ddl in TABLES01.iteritems():
        try:
            #cursor.execute("DROP TABLE IF EXISTS ".join(name))
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")






def random_digits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)

def random_birthday():
    year = random.randint(1950, 1995)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)

    birthday = str(year) + str(month) + str(day)
    return birthday

def random_time():
    year = random.randint(2017, 2017)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)

    hour = random.randint(9, 22)
    min_ = random.randint(0, 59)
    sec_ = random.randint(0, 59)
    if hour < 10:
        hour = '0' + str(hour)
    if min_ < 10:
        min_= '0' + str(min_)
    if sec_ < 10:
        sec_ = '0' + str(sec_)

    time_ = str(year) + str(month) + str(day) + str(hour) + str(min_) +str(sec_)
    return time_


def create_main_table_data():
    for i in range(0,HOSPITAL_MANY):
        hospitalID_array.append(''.join(random.choice(string.lowercase) for x in range(random.randint(5, 5))))
    for i in range(0,DOCTOR_MANY):
        doctorID_array.append(''.join(random.choice(string.lowercase) for x in range(random.randint(5, 5))))
    for i in range(0,NURSE_MANY):
        nurseID_array.append(''.join(random.choice(string.lowercase) for x in range(random.randint(5, 5))))
    for i in range(0,SUBJECTLIST_MANY):
        subjectID_array.append(''.join(random.choice(string.lowercase) for x in range(random.randint(5, 5))))
    for i in range(0,USER_MANY):
        userID_array.append(''.join(random.choice(string.lowercase) for x in range(random.randint(5, 5))))
    for i in range(0,OFFICE_MANY):
        office_array.append(str(random.randint(1, 9)*100+random.randint(1, 9)))
    for i in range(0,ROOMNUMBER_MANY):
        roomNumber_array.append(str(random.randint(1, 30)*100+random.randint(1, 9)))

    print roomNumber_array
    print office_array
    print userID_array
    print subjectID_array
    print nurseID_array
    print doctorID_array
    print hospitalID_array


def create_dummy_data(i):
    pre_address_template = ['서울', '부산', '인천', '울산', '대전', '대구', '광주', '제주']
    pre_gender_template = ['MALE', 'FEMALE']
    pre_name01_template = [u'김',u'김',u'김',u'김',u'김',u'김',u'김',u'고',u'한',u'이',u'이',u'이',u'조',u'박',u'박',u'박',u'박',
                        u'오',u'오',u'최',u'최',u'최',u'최',u'윤',u'윤',u'윤',u'하',u'하',u'하',u'남',u'남',u'유',u'정',u'정',u'강',u'강',u'남',
                        u'허']
    pre_name02_template = [u'지',u'영',u'재',u'효',u'윤',u'정',u'현',u'광',u'규',u'말',u'고',u'희']
    pre_name03_template = [u'미',u'민',u'범',u'철',u'수',u'은',u'성',u'수',u'근',u'환',u'자',u'순',u'희',u'진',u'아']
    pre_bloodType_template = ['A', 'B', 'O', 'AB']
    pre_hospital01_name=['멋진','귀여운','최고','건강','관리','짱','이','모든','굿','감동','사랑','마음','스페셜','왕','저렴']
    pre_hospital02_name=['서비스','한양','수술','의과','고려','연세','서울','중앙','숭실','성균관','서강']
    pre_hospital03_name=['병원', '의원', '병동', '보건소']
    #subjectName = subject_name_array[i%SUBJECT_MANY]
    pre_myRank_template = ['S++','S', 'A+', 'B+', 'C+']
    #ID = ''.join(random.choice(string.lowercase) for x in range(random.randint(5, 5)))
    password = ''.join(random.choice(string.lowercase) for x in range(random.randint(6, 10)))
    name = random.choice(pre_name01_template)+random.choice(pre_name02_template)+random.choice(pre_name03_template)
    birthday = random_birthday()
    address = random.choice(pre_address_template)
    phone = "010"+str(random_digits(8))
    phoneFamily = "010"+str(random_digits(8))
    gender = random.choice(pre_gender_template)
    bloodType = random.choice(pre_bloodType_template)
    myRank = random.choice(pre_myRank_template)
    #doctorID = doctorID_array[i]
    doctorID_sub = doctorID_array[i%DOCTOR_MANY]
    #nurseID = nurseID_array[i]
    nurseID_sub = nurseID_array[i%NURSE_MANY]
    #userID = userID_array[i]
    userID_sub = userID_array[i%USER_MANY]
    #subjectID = subjectID_array[i]
    subjectID_sub = subjectID_array[i%SUBJECTLIST_MANY]
    #hospitalID = hospitalID_array[i]
    hospitalID_sub = hospitalID_array[i%HOSPITAL_MANY]
    #office=office_array[i]
    office_sub=office_array[i%OFFICE_MANY]
    #roomNumber=roomNumber_array[i]
    roomNumber_sub=roomNumber_array[i%ROOMNUMBER_MANY]
    appoint_time=random_time()
    subjectName=random.choice(subject_name_array)
    subjectNamelist=subject_name_array[i%SUBJECTLIST_MANY]
    hospitalName = random.choice(pre_hospital01_name)+random.choice(pre_hospital02_name)+random.choice(pre_hospital03_name)
    location = random.choice(pre_address_template)
    totalMoney = random.randint(100, 100000)
    score = random.randint(1, 5)
    temperature = random.randint(0, 9)/10.0 + random.randint(35, 36)
    heartRate = random.randint(60, 100)
    bloodPressure = random.randint(80, 130)
    distance = random.randint(1, 503)

    if index==1:
        temp_tuple01 = (userID_sub, password, name, birthday, address, phone, phoneFamily, gender, bloodType, myRank )
        print temp_tuple01
        return  temp_tuple01
    elif index==  2:
        temp_tuple02 = (hospitalID_sub, hospitalName, location)
        print temp_tuple02
        return  temp_tuple02
    elif index==  3:
        temp_tuple03 = (subjectID_sub, subjectNamelist)
        print temp_tuple03
        return  temp_tuple03
    elif index==  4:
        temp_tuple04 = (doctorID_sub, hospitalID_sub, name, birthday, gender, subjectID_sub, myRank)
        print temp_tuple04
        return  temp_tuple04
    elif index==  5:
        temp_tuple05 = (hospitalID_sub, subjectID_sub)
        print temp_tuple05
        return  temp_tuple05
    elif index==  6:
        temp_tuple06 = (hospitalID_sub, subjectID_sub, office_sub, roomNumber_sub, doctorID_sub)
        print temp_tuple06
        return  temp_tuple06
    elif index==  7:
        temp_tuple07 = (doctorID_sub, userID_sub)
        print temp_tuple07
        return  temp_tuple07
    elif index==  8:
        temp_tuple08 = (nurseID_sub, hospitalID_sub, name, birthday, gender, myRank)
        print temp_tuple08
        return  temp_tuple08
    elif index==  9:
        temp_tuple09 = (hospitalID_sub, userID_sub, totalMoney)
        print temp_tuple09
        return  temp_tuple09
    elif index==  10:
        temp_tuple10 = (userID_sub, hospitalID_sub, distance)
        print temp_tuple10
        return  temp_tuple10
    elif index==  11:
        temp_tuple11 = (doctorID_sub, userID_sub, score)
        print temp_tuple11
        return  temp_tuple11
    elif index==  12:
        temp_tuple12 = (hospitalID_sub, userID_sub, score)
        print temp_tuple12
        return  temp_tuple12
    elif index==  13:
        temp_tuple13 = (userID_sub, location, temperature, heartRate, bloodPressure)
        print temp_tuple13
        return  temp_tuple13
    elif index==  14:
        temp_tuple14 = (doctorID_sub, userID_sub, appoint_time)
        print temp_tuple14
        return  temp_tuple14


def insert_tables():
    add_query01 = ("INSERT INTO User (ID, password, name, birthday, address, phone, phoneFamily, gender, bloodType, myRank) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    add_query02 = ("INSERT INTO Hospital (hospitalID, hospitalName, location) VALUES (%s, %s, %s)")
    add_query03 = ("INSERT INTO Medical_subject_list (subjectID, subjectName) VALUES (%s, %s)")
    add_query04 = ("INSERT INTO Doctor (doctorID, hospitalID, name, birthday, gender, subjectID, myRank) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    add_query05 = ("INSERT INTO Medical_subject (hospitalID, subjectID) VALUES (%s, %s)")
    add_query06 = ("INSERT INTO OfficeBuilding (hospitalID, subjectID, office, roomNumber, doctorID) VALUES (%s, %s, %s, %s, %s)")
    add_query07 = ("INSERT INTO Favorite (doctorID, userID) VALUES (%s, %s)")
    add_query08 = ("INSERT INTO Nurse (nurseID, hospitalID, name, birthday, gender, myRank) VALUES (%s, %s, %s, %s, %s, %s)")
    add_query09 = ("INSERT INTO Support (hospitalID, userID, totalMoney) VALUES (%s, %s, %s)")
    add_query10 = ("INSERT INTO Distance (ownerID, hospitalID, distance) VALUES (%s, %s, %s)")
    add_query11 = ("INSERT INTO Review_doctor (doctorID, userID, score) VALUES (%s, %s, %s)")
    add_query12 = ("INSERT INTO Review_hospital (hospitalID, userID, score) VALUES (%s, %s, %s)")
    add_query13 = ("INSERT INTO Smartband (ownerID, location, temperature, heartRate, bloodPressure) VALUES (%s, %s, %s, %s, %s)")
    add_query14 = ("INSERT INTO Appointment_table (doctorID, patientID, appoint_time) VALUES (%s, %s, %s)")



    global index
    for i in range(0,USER_MANY):
        cursor.execute(add_query01, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,HOSPITAL_MANY):
        cursor.execute(add_query02, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,SUBJECTLIST_MANY):
        cursor.execute(add_query03, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,DOCTOR_MANY):
        cursor.execute(add_query04, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,SUBJECT_MANY):
        cursor.execute(add_query05, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,OFFICE_MANY):
        cursor.execute(add_query06, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query07, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,NURSE_MANY):
        cursor.execute(add_query08, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query09, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query10, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query11, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query12, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query13, (create_dummy_data(i)))
    index=index+1
    conn.commit()
    for i in range(0,MAX_LOOP):
        cursor.execute(add_query14, (create_dummy_data(i)))
    index=index+1
    conn.commit()



if __name__ == '__main__':
    create_tables()
    create_tables01()
    create_main_table_data()
    insert_tables()
