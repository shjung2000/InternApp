<h1 align = "center"> Welcome to our InternApp Application 📝 </h1>
<p align = "center">
  This application aims to help connect companies 🕴️ and SMU students 🧑‍🎓 on internship roles. Any interested companies that are currently looking for interns can use this app. SMU students can then apply for internships from this app directly. 
 
</p>

****

<p align="center">
  <img width="900" height="650" src="https://github.com/asianburpgirl/internapp/blob/main/frontend/img/bgpg.jpg"></img>
</p>


 <h1 align = "center"> Step by Step guide on How to Use Our Application </h3>

# 1. Prerequisite Requirements
1. WAMP (Windows User) / MAMP (Mac User) 🐘
2. Docker 🐳
3. Postman 📮


# 2. How to start running our application (Step by Step)
1. Ensure both Docker and MAMP/WAMP are running
2. Go to http://localhost/phpmyadmin/index.php. Login with -- **Username**: is213 **Password**: -leave blank- For mac and linux users, **Password**: root
3. Import sql files from internapp folder to create the necessary databases to connect and interact with our application.
4. Open Visual Studio Code and open the folder *internapp*
***
5. <h2 align = "center">❗❗❗❗ IMPORTANT ❗❗❗❗</h2>
* In the ***docker-compose.yml*** file, port number for each **dbURL** header of every microservice should be 3306. For eg, **dbURL**: mysql+mysqlconnector://is213@host.docker.internal:**3306**/student 
* Please **REMOVE** all the ***images*** and ***containers*** from your own docker engine before starting up to avoid port conflicts
***
6. Run the docker by entering **docker-compose up** into the terminal
7. Once the images are built up, you can access the html files and test out the application service

### 3. Setting up kong routing for application microservice
1. cd kong at internapp directory
2. docker-compose up 
3. Access http://localhost:1337 and log in to your KONGA account. 
-username: admin
-email : <use smu email>
-password: adminadmin
4.When you see "Welcome" , 
-Name:deafult
-Kong Admin URL: http://kong:8001
-Press "Create Connection"
4. Add new service
-Name: applicationapi
-Url: http://application1:5001/application
5. Add new route
-Click on applicationapi service, then the Route tab, Add new route
-Paths: /api/v1/application   (press enter)
-Methods: GET POST PUT   (press enter after each method) 
- Click 'Submit Route'
5. Run command in terminal:
docker run --rm -d --name=application1 --network=kong_kong-net -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/application shchong/application:esd
6. Check if http://localhost:8000/api/v1/application returns database. 

# 4. Testing of the microservices
### If you wish to test out each microservices (Simple or Complex) one by one, please do the following:
1. Open your Postman
2. Click [here](https://drive.google.com/drive/folders/1ljK9z3G1IR7Gf_BBsFyozS2YVvN7uExM?usp=sharing) to see all the API documents which will show you the **expected output** you should see when testing out the specific **inputs** , **service URL** and **methods** for every simple and complex microservices.







