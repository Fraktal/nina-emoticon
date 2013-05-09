NINA LAB
========


The **emoticon-project** is a sentiment analysis web app using machine learning methods such as K-means and K nearest neighbor to link tweets with emoticons to track sentiment

This code is being developed by the NINA Lab at the **University of North Carolina Asheville**. This application
is in development. Please be aware of this as you look at the code. 



Installation  
------------  
  
  
  
To install **emoticon-project** via git open terminal. Once you have terminal open, type in the command     

    git clone git@github.com:Fraktal/emoticon-project.git

Once you have the repository cloned, run these commands...  
 
    cd emoticon-project
    npm init

After you run npm init, just hit enter until you get past the questions. Now, run these commands...  

    cd app
    npm install       

Immortal-ntwitter is not part of the npm install, so...       

    cd node_modules
    git clone https://github.com/horixon/immortal-ntwitter.git

Now, of course, you will have to move your twitter credentials.js file to the app directory in   
the project.     

Since the app.js file is not really configured to run, you have to be in the app directory and then   

    node tracker.js

That should send a stream of tweets flowing down your terminal.  



**REMINDER:** This app is under construction and exists in a constant state of development    