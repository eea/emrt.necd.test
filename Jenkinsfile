pipeline {

	agent { dockerfile true }

	stages {
		node {
			def app

			stage('Build image') {
		    	app = docker.build("getintodevops/hellonode")
	    	}

	    	stage('Test image') {
       
		        app.inside {
		            sh 'echo "Tests passed"'
		        }
    		}
		}
		
    }
}
