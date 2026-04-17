import requests
from bs4 import BeautifulSoup
import csv
class OAUportal:

    
   
    def __init__(self):
        ...
        

    # Function to login into the portal and create a session for the user
    def login(self,username,password,year=2024,semester=1):
        self.username=username
        self.password=password
        self.year=year
        self.semester=semester
        self.session=requests.Session()
            

        login_url="https://eportal.oauife.edu.ng/login.php"
        login=self.session.get(login_url)
    
        payload={
            "user_id":self.username,
            "pswd":self.password,
            "SessionF":self.year,
            "SemesterF":self.semester,
            "Submit":"Submit"
        }

        headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'Connection':'keep-alive',
            'Referer':'https://eportal.oauife.edu.ng/undergraduatetasks.php',
            'Origin':'https://eportal.oauife.edu.ng'
        }
        print("Logging in...")
        submit_url="https://eportal.oauife.edu.ng/login1.php"
        
        response=self.session.post(submit_url,data=payload,headers=headers)


        if "profile" in response.text:
            print("Login successful")
        else:
            print("Login unsuccessful")   
            
        print(response.status_code)

    def get_raw_score(self):
        raw_url="https://eportal.oauife.edu.ng/viewrawscore1.php"
        print("Getting raw score...")
        raw_response=self.session.get(raw_url)
        soup=BeautifulSoup(raw_response.text,'html.parser')
        table=soup.find('table',class_='profile')
        if table:
            obe=table.find_all('tr')
            for cell in obe[1:]:
                course_code=cell.find_all('td')[0].text.strip()
                score=cell.find_all('td')[-1].text.strip()
                print(f'Course: {course_code} Score: {score}')
        else:
            print(raw_response.text)
            print (raw_response.url)
            print("Element not found")
                    
    def course_reg(self):
        courses={}
        course_url='https://eportal.oauife.edu.ng/courseform1.php' # course form url
        course_res=self.session.get(course_url) # To navigate to the course form url
        course2_url='https://eportal.oauife.edu.ng/courseform2.php'

        soup=BeautifulSoup(course_res.text,'html.parser')
        table=soup.find('table',class_='profile')
        if table:
            tuple=table.find_all('tr')
            for cell in tuple[1:]:
                code=cell.findall('td')[0].text.strip()
                courses[code]='1'
            print(courses)
        else:
            print('Course Form not found')
            print(f'{course_res.url} | {course_res.status_code}')
        submit_res=self.session.post(course2_url,data=courses) # submit the course form
        if submit_res.text:
            registered_courses=True

        def delete_courses(self):
            if registered_courses:
                ...
            else:
                ...
    # To get resutls
    def get_results(self,session='All',year='1'):
        result_url='https://eportal.oauife.edu.ng/result_check1.php'
        initial_res=self.session.get(result_url)
        get_results_url='https://eportal.oauife.edu.ng/result_check2.php'
        data={
            'Session':session,
            'Semester':year,
            'Command1':'Check Results'
        }
        display_res=self.session.post(get_results_url,data=data)
        print(f'{display_res.url} | {display_res.status_code}')
        results=BeautifulSoup(display_res.text,'html.parser')
        tot_results=results.find_all('table')
    
        for sem in tot_results[0::2]:
            rows=sem.find_all('tr')
            for row in rows:
                print(row[-1]).text.strip()
                
        def save(self,file):
            with open (file,'w',newline='') as res_score:
                columns=['Course code','Course unit','Score']
                writer=csv.Dictwriter(res_score,fieldnames=columns)
                writer.writeheader()
                writer.writerows[row]
                print("Data successfully written into results.csv")


