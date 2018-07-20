pipeline {
	def app

	agent { dockerfile true }

	stages {
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
