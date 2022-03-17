# Project Vaccination...
import datetime
from datetime import date
import mysql.connector as msc
import random
while True:
    pswrd=input('Enter your password of your mysql database..')
    try:
        db=msc.connect(user='root',host='localhost',password=pswrd)
        break
    except:
        print('Wrong password or May be Another technical error..')
cur=db.cursor()
days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def date_time_day(x):
    now=datetime.datetime.now()
    dat=date.today()
    if x=='t' :
        return now.strftime('%H:%M:%S')
    elif x=='d': 
        return dat
    elif x=='D' :
        return list(dat.isocalendar())[-1]   


def registration(cur,typ):
    if typ=='2':
        slot=int(input('Enter your Slot Number..'))
    else :
        slot=typ
    cur.execute('SELECT * FROM SLOTS WHERE SLOT_NUM={}'.format(slot))
    data=list(cur)
    cur.execute('SELECT * FROM _INFO_ WHERE REG_ID={}'.format(slot))
    ch_dta=list(cur)
    if data==[] :
        print('No Booked SLOT found please book your slot first..')
        return None
    else :
        if ch_dta==[]:
            while True :
                name=input('Enter your Name that you have entered at the time of Slot BOOKING..').title()
                if name.lower()==data[0][2].lower():
                    print('Varification Successfull..')
                    print('Fill up these details and get Vaccinated..')
                    break
                else :
                    print('Wrong Information..')
                    ch=input('Wants To try again..(y/n)').lower()
                    if ch=='n':
                        break
        else :
            print('You Are already Vaccinated..')
            return None
    dob=input("Enter your Date of birth in 'YYYY-MM-DD' format..")
    email=input('Enter your E-mail address..').lower()
    adrs=input('Enter your Home address..')
    pin_code=int(input('Enter pin code of yout area..'))
    adhr_num=int(input('Enter your 16 digit Adhar number without space..'))
    cur.execute('SELECT DOCTOR_NAME FROM DOC_INFO')
    names=list(cur)
    sel=random.choice(names)
    doc=names.index(sel)
    print('You will be vaccinated by',sel[0])
    try:
        
        cur.execute("INSERT INTO _INFO_ VALUES({},'{}','{}','{}','{}',{},'{}','{}','{}','{}','{}')".format(slot,name,dob,email,adrs,pin_code,adhr_num,doc,date_time_day('d'),date_time_day('t'),date_time_day('D')))
        db.commit()
    except Exception as e:
        print(e)
    print('*************************************************************')
    print('**Registration Successfull..                                                                    **')
    print('**CONGRATULATIONS!! VACCINATION SUCCESSFULL   **')
    print('*************************************************************')
    print('YOU CAN DOWLOAD YOUR CERTIFICATE FROM DOWLOAD MENU..BY FILLING SOME DETAILS..')
    
def isdbexist(cur):
    try:
        cur.execute('CREATE DATABASE COV_VACCI_SOFT;')
        cur.execute('USE COV_VACCI_SOFT;')
        cur.execute('CREATE TABLE _INFO_(REG_ID INT PRIMARY KEY,NAME VARCHAR(30),DOB DATE,EMAIL VARCHAR(50),HOME_ADRS VARCHAR(50),PINCODE INT,ADHAR_NUMBER CHAR(16),DOC_COD CHAR(1),DAT_O_VACC DATE, TIME_O_VACC TIME,DAY CHAR(1));')
        cur.execute("CREATE TABLE SLOTS(SLOT_NUM INT PRIMARY KEY,MO_NUMBER CHAR(10),NAME VARCHAR(30),VACC_TYP CHAR(20));")
        cur.execute("CREATE TABLE DOC_INFO(DOCTOR_NAME VARCHAR(40),STAFF CHAR(20));")
        cur.execute("INSERT INTO DOC_INFO VALUES('Dr. Sanjeev Kumar','NURSH'),('Dr. Abir Ghosh','NURSH'),('Dr. Priyojit Bagchi','NURSH');")
        db.commit()
    except Exception as e:
        print(e)
        cur.execute('USE COV_VACCI_SOFT')
        cur.execute('DROP DATABASE COV_VACCI_SOFT')
        db.commit()
        isdbexist(cur)


def slots(cur):
    num=int(input('Enter your Mobile Number..\nOnly 4 person can use a number for vaccination :-'))
    cur.execute('SELECT COUNT(*) FROM SLOTS GROUP BY MO_NUMBER HAVING MO_NUMBER ="{}"'.format(num))
    rec=list(cur)
    if rec==[]:
        co=0
    else :
        co=int(rec[0][0])
    if co>=4:
        print('Please use another number onlt 4 person can use a number..')   
    else :
        if rec==[]:
            nam=input('Enter your Name..').title()
        else:
            nam=input('Enter your Name..').title()
            cur.execute("SELECT * FROM SLOTS WHERE NAME='{}' AND MO_NUMBER='{}'".format(nam,num))
            da=list(cur)
            if da==[]:
                pass
            else :
                print('You are already Vaccinated')
                return None
        vaccine=['COVAXIN','COVID SHIELD','BOSTER DOSE']
        print('Choose your Vaccine..')
        for i in range(len(vaccine)):
            print(i+1,'.',vaccine[i])
        while True:
            ch=input('Enter your choice here in numberic form..')
            if ch in'123':
                ch=int(ch)
                break
            print('Wrong Input..')
        cur.execute('SELECT * FROM SLOTS')
        data=list(cur)
        if data==[]:
            slot=1
        else :
            slot=int(data[-1][0])+1
            
        cur.execute("INSERT INTO SLOTS VALUES({},'{}','{}','{}')".format(slot,num,nam,vaccine[ch-1]))
        db.commit()
        #Completed..
        print('*******************************')
        print('*YOUR SLOT NUMBER IS',slot)
        print('*******************************')
        ch=input('Are you want to get vaccinated Now..(y/n)...').lower()
        if ch=='y':
            registration(cur,slot)
        else :
            print('your Slot is Booked you can register and get vaccinated by choosing second option...\n ') 
    
def main(cur):
    print('VACCINATION SLOT BOOKING AND REGISTRATION...')
    print('1. SLOT BOOKING...')
    print('2. ALREADY BOOKED SLOT WANT TO DO REGISTRATION...')
    print('3. DOWNLOAD CERTIFICATE..')
    print('4. EXIT...')
    while True:
        cho=input('Enter your Choice in Numeric Form..')
        if cho in '1234':
            cho=int(cho)
            break
        else:
            print('Wrong Choice...')
    if cho==1:
        slots(cur)
    elif cho==2:
        registration(cur,'2')
    elif cho==3:
        certificate(cur)
    elif cho==4:
        exit()
        
def certificate(cur):
    slot=int(input('Enter Your Slot number. '))
    cur.execute('SELECT * FROM SLOTS WHERE SLOT_NUM={}'.format(slot))
    y=list(cur)
    if y==[]:
        print('No booking found by this slot number...')
    else :
        vcc=y[0][-1]
        cur.execute('SELECT * FROM _INFO_ WHERE REG_ID={}'.format(slot))
        z=list(cur)
        if z==[]:
            print('YOU ARE NOT STILL VACCINATED..')
            print('Choose second option from main menu for vaccination..')
            return None
            print()
        else :
            nam=input('Enter your name that u had enterd at the time of vaccination.. for verification..').lower()
            if nam==z[0][1].lower():
                print('Varification successful...')
                print()
            else :
                print('Verification Failed wrong information')
                print()
                return None
            dob,dov,tov=z[0][2],z[0][-3],z[0][-2]
            cur.execute('SELECT DOCTOR_NAME FROM DOC_INFO')
            do=list(cur)
            doctor=do[int(z[0][-4])][0]
            print('''    *******************************************
    +*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
    +>+>+>>>>VACCINATION CERTIFICATE<<<<<<+<+<+
    Name:{}    DATE_OF_BIRTH:{}
    VACCINE_TYPE:{}   TIME_OF_VACCINATION:{}
    ADHAR_NUMBER:{}
    DATE_OF_VACCINATION:{}
    VACCINATED BY DOCTOR:{}  ON:{}
    HOME_ADDRESS:{}
    PINCODE:{}       SLOT_NUMBER:{}
    +*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*
    **************************************************'''.format(z[0][1],dob,vcc,tov,z[0][-5],dov,doctor,days[int(z[0][-1])-1],z[0][4],z[0][5],z[0][0]))

if __name__=='__main__':
    try:
        cur.execute('USE COV_VACCI_SOFT')
    except:
        isdbexist(cur)
        cur.execute('USE COV_VACCI_SOFT')
    while True:
        main(cur)
        db.commit()
        
db.close()