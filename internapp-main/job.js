const express=require('express');
const cors = require('cors')
const bodyParser=require('body-parser');
const app=express();
const mysql=require('mysql');
app.use(cors());
app.use(bodyParser.json());

var conn = mysql.createConnection({
    // for when deployed to dockers
    //host: "host.docker.internal",
    // for local machine 
    host: "host.docker.internal",
    user: "root",
    password: "",
    database: "job",
    
});



/**
 * Get All jobs
 *
 */
app.get('/job',function(req,res){
    let sqlQuery = "SELECT * FROM job";
    
    let query = conn.query(sqlQuery, (err, results) => {
       
        res.send(apiResponse(results));
  });
});
/**
 * Search for Specific Job
 *
 */

app.get('/job/:jobID',function(req,res){
    let sqlQuery = "SELECT * FROM job WHERE jobID="+req.params.jobID;
  
    let query = conn.query(sqlQuery, (err, results) => {
        
        res.send(apiResponse(results));
  });
});

/**
 * Create new job posting
 * check_job
 */


app.get('/job_check',function(req,res){
    let sqlQuery = "SELECT * FROM job WHERE jobID="+req.body.jobID;  
    let query = conn.query(sqlQuery, (err, results) => {
        
        res.send(apiResponse(results));
});
});
/**
 * Create new job posting
 *
 */


app.post('/job/:jobID',function(req,res){
    let data={jobID: req.params.jobID , companyID: req.body.companyID, jobName: req.body.jobName, postDate: req.body.postDate, jobDesc: req.body.jobDesc, deadline: req.body.deadline}
    let sqlQuery = "INSERT INTO job SET ?";
    let query = conn.query(sqlQuery, data,(err, results) => {
       
        res.send(apiResponse(data));
    });
});



/**
 * Update posting
 *
 */
 app.put('/job/:jobID',(req, res) => {
    let sqlQuery = "UPDATE job SET jobName='"+req.body.jobName+"', postDate='"+req.body.postDate+"',jobDesc='"+req.body.jobDesc+"',deadline='"+req.body.deadline+"' WHERE jobID="+req.body.jobID+"";

    let query = conn.query(sqlQuery, (err, results) => {
        res.send(apiResponse(results));
    });
});







/**
 * Delete posting
 *
 */

 app.delete('/job/:jobID',function(req,res){
    let sqlQuery = "DELETE FROM job WHERE jobID="+req.body.jobID+"";
    let query = conn.query(sqlQuery, (err, results) => {
        res.send(apiResponse(results));
    });

})



/**
 * API Response 
 *
 */

function apiResponse(results){
    return JSON.stringify({"code": 201, "data": results});
}

app.listen(5003,() =>{
    console.log('Server started on port 5003.ahds..');
});